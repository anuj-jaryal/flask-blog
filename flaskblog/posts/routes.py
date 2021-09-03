from flask import  render_template, url_for,flash, redirect, request, abort,Blueprint
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post,Tag
from flaskblog import db
from flask_login import current_user, login_required
from pprint import pprint


posts = Blueprint('posts', __name__)


@posts.route('/post')
@login_required
def index_post():
    page = request.args.get('page',1,type=int)
    posts =Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page = page)
    return render_template('posts/index.html', posts=posts)

@posts.route('/user/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts =Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(per_page=5,page = page)
    return render_template('posts/user_posts.html', posts=posts,user=user)

@posts.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('name')]
    if form.validate_on_submit():
        #pprint(form.tags.data)
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        for id in form.tags.data:
            post.tags.append(Tag.query.get(id))
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect( url_for('posts.index_post'))
    return render_template('posts/create.html', form=form)

@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post =Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post =Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('name')]
    if form.validate_on_submit():
        post.title= form.title.data 
        post.content=form.content.data
        
        for ptag in post.tags:
            post.tags.remove(ptag)

        for id in form.tags.data:
            tag = Tag.query.get(id)
            post.tags.append(tag)
                   
        db.session.commit()
        flash('Post Update successfully', 'success')
        return redirect( url_for('posts.post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = [(tag.id)for tag in post.tags]
    return render_template('posts/update.html', form =form)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post =Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect( url_for('posts.index_post'))
