from flask import url_for , render_template , redirect , flash , Blueprint , request
from flask_login import login_user, current_user,logout_user,login_required
from app import db
from app.models import User,Post,Reaction
from app.forms import LoginForm,RegistrationForm,PostForm
from werkzeug.security import generate_password_hash, check_password_hash

main=Blueprint('main',__name__)


@main.route('/')
@main.route('/home')
def home():
    posts=Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html',posts=posts)

@main.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form=RegistrationForm()

    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)

        user=User(username = form.username.data,
                  email = form.email.data,
                  password = hashed_password)

        db.session.add(user)
        db.session.commit()
        flash('Account created !You can login now .','success')
        return redirect(url_for('main.login'))
    return render_template('register.html',form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Check email and password!', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    print("FORM SUBMITTED:", form.validate_on_submit())
    print("FORM ERRORS:", form.errors)
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('POSTED', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', form=form)

@main.route('/post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        flash('You can only delete your post !','danger')
        return redirect(url_for('main.home'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted !','success')
    return redirect(url_for('main.home'))

@main.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You can only edit your own posts!', 'danger')
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('Content cannot be empty!', 'danger')
            return render_template('edit_post.html', post=post)
        post.content = content
        db.session.commit()
        flash('Post updated! ✅', 'success')
        return redirect(url_for('main.home'))
    return render_template('edit_post.html', post=post)

@main.route('/post/<int:post_id>/react/<emoji>',methods=['POST'])
@login_required
def react_post(post_id,emoji):
    post=Post.query.get_or_404(post_id)
    existing=Reaction.query.filter_by(
        user_id=current_user.id,
        post_id=post_id,
        emoji=emoji
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
    else:
        reaction=Reaction(
            emoji=emoji,
            user_id=current_user.id,
            post_id=post_id

        )
        db.session.add(reaction)
        db.session.commit()
    return redirect(url_for('main.home'))


