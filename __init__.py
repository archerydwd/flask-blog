import sqlite3
from flask import Flask, render_template, url_for, request, redirect, flash, g, session

app = Flask(__name__)

SQL = """
create table if not exists articles (
  	article_id INTEGER PRIMARY KEY AUTOINCREMENT,
	  article_title varchar(24),
		article_text varchar(200)
		)
"""

COMMENT = """
create table if not exists comments (
	comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
	art_id INTEGER,
	commenter varchar(50),
	body varchar(250),
	FOREIGN KEY(art_id) REFERENCES articles(article_id)
	)
"""

def setupdb():
	with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
		cursor = connection.cursor()
		cursor.execute(SQL)
		cursor.execute(COMMENT)

setupdb()

@app.route('/', methods=['GET', 'POST'])
def display_articles():
	with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
		cursor = connection.cursor()
		SELECT = """SELECT * from articles"""
		articles_data = cursor.execute(SELECT)
	return(render_template("index.html", the_title="Flask Blog", articles=articles_data, delete_link=url_for("delete_article"), update_link=url_for("update_article"), show_link=url_for("show_article"), create_link=url_for("create_article")))

@app.route('/articles/create', methods=['GET', 'POST'])
def create_article():
	return(render_template("create.html", the_title="Flask Blog - create", index_link=url_for("display_articles"), save_article_link=url_for("save_article")))
					
@app.route('/savearticle', methods=['POST'])
def save_article():
	all_ok = True
	if len(request.form['article_title']) < 5:
		all_ok = False
		flash("Sorry the article title must be 5 or more characters. Try again")
	if len(request.form['article_title']) == 0:
		all_ok = False
		flash("Sorry the article title cannot be empty. Try again")
	if len(request.form['article_text']) == 0:
		all_ok = False
		flash("Sorry the article text cannot be empty. Try again")
	if all_ok:
		with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
			cursor = connection.cursor()
			INSERT = """
			INSERT INTO articles (article_title, article_text) 
			VALUES (?, ?)
			"""
			cursor.execute(INSERT, (request.form['article_title'], request.form['article_text']))
			SELECT = """
			SELECT * from articles
			"""
			articles_data = cursor.execute(SELECT)
		return(render_template("index.html", the_title="Flask Blog", articles=articles_data, delete_link=url_for("delete_article"), update_link=url_for("update_article"), show_link=url_for("show_article"), create_link=url_for("create_article")))
	else:
		return(redirect(url_for("create_article")))

@app.route('/articles/show', methods=['POST'])
def show_article():
	with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
		cursor = connection.cursor()
		SHOW = """SELECT * FROM articles WHERE article_id == (?)"""
		SHOWCOMMENTS = """SELECT * FROM comments WHERE art_id == (?)"""
		article_data = list(cursor.execute(SHOW, (request.form['article_id'],)))
		articles_comments = list(cursor.execute(SHOWCOMMENTS, (request.form['article_id'],)))
	return(render_template("show.html", the_title="Flask Blog - show", article=article_data, comments=articles_comments, index_link=url_for("display_articles"), delete_link=url_for("delete_article"), update_link=url_for("update_article"), delete_comment_link=url_for("delete_comment"), create_comment_link=url_for("create_comment")))

@app.route('/articles/delete', methods=['POST'])
def delete_article():
	with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
		cursor = connection.cursor()
		DELETE = """DELETE FROM articles WHERE article_id == (?)"""
		DELETECOMMENTS = """DELETE FROM comments WHERE art_id == (?)"""
		cursor.execute(DELETE, (request.form['article_id'],))
		cursor.execute(DELETECOMMENTS, (request.form['article_id'],))
	return(redirect(url_for("display_articles")))

@app.route('/articles/update', methods=['GET', 'POST'])
def update_article():
	with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
		cursor = connection.cursor()
		ARTICLE = """SELECT * FROM articles WHERE article_id == (?)"""
		article_data = cursor.execute(ARTICLE, (request.form['article_id'],))
	return(render_template("update.html", the_title="Flask Blog - update", article=article_data, index_link=url_for("display_articles"), changes_link=url_for("save_changes")))

@app.route('/articles/update_save', methods=['POST'])
def save_changes():
	with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
		cursor = connection.cursor()
		UPDATE = """UPDATE articles SET article_title = ?, article_text = ? WHERE article_id == ?"""
		cursor.execute(UPDATE, (request.form['article_title'], request.form['article_text'], request.form['article_id']))
		SELECT = """SELECT * from articles"""
		articles_data = cursor.execute(SELECT)
	return(render_template("index.html", the_title="Flask Blog", articles=articles_data, delete_link=url_for("delete_article"), update_link=url_for("update_article"), show_link=url_for("show_article"), create_link=url_for("create_article"))) 

@app.route('/comments/create', methods=['POST'])
def create_comment():
	all_ok = True
	if len(request.form['commenter']) == 0:
		all_ok = False
		flash("Sorry your name cannot be empty. Try again")
	if len(request.form['body']) == 0:
		all_ok = False
		flash("Sorry your comment cannot be empty. Try again")
	if all_ok: 
		with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
			cursor = connection.cursor()
			INSERT = """
				INSERT INTO comments (art_id, commenter, body) 
				VALUES (?, ?, ?)
				"""
			cursor.execute(INSERT, (request.form['article_id'], request.form['commenter'], request.form['body']))
			ARTICLE = """SELECT * FROM articles WHERE article_id == (?)"""
			SELECT = """SELECT * from comments WHERE art_id == (?)"""
			article_data = list(cursor.execute(ARTICLE, (request.form['article_id'],)))
			comments_data = list(cursor.execute(SELECT, (request.form['article_id'],)))
		return(render_template("show.html", the_title="Flask Blog - show", article=article_data, comments=comments_data, index_link=url_for("display_articles"), delete_link=url_for("delete_article"), update_link=url_for("update_article"),  delete_comment_link=url_for("delete_comment"), create_comment_link=url_for("create_comment")))
	else:
		return(redirect(url_for("show.html")))

@app.route('/comments/delete', methods=['POST'])
def delete_comment():
	with sqlite3.connect('blogdata.db', check_same_thread=False) as connection:
		cursor = connection.cursor()
		DELETE = """DELETE FROM comments WHERE comment_id == (?)"""	
		ARTICLE = """SELECT * FROM articles WHERE article_id == (?)"""
		SELECT = """SELECT * from comments WHERE art_id == (?)"""
		cursor.execute(DELETE, (request.form['comment_id'],))
		article_data = list(cursor.execute(ARTICLE, (request.form['article_id'],)))
		comments_data = list(cursor.execute(SELECT, (request.form['article_id'],)))
	return(render_template("show.html", the_title="Flask Blog - show", article=article_data, comments=comments_data, index_link=url_for("display_articles"), delete_link=url_for("delete_article"), update_link=url_for("update_article"),    delete_comment_link=url_for("delete_comment"), create_comment_link=url_for("create_comment")))

app.config['SECRET_KEY'] = 'thisismysecretkeywhichyouwillneverguesshahahahahahahahaha'
if __name__ == "__main__":
	app.run()

