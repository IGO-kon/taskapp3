from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# モデル定義
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Item {self.name}>'

# ルート
@app.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    total_items = Item.query.count()
    total_quantity = db.session.query(db.func.sum(Item.quantity)).scalar() or 0
    low_stock = Item.query.filter(Item.quantity < 10).count()
    return render_template('index.html', 
                         items=items, 
                         total_items=total_items,
                         total_quantity=total_quantity,
                         low_stock=low_stock)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = request.form.get('quantity', type=int)
        price = request.form.get('price', type=float)
        category = request.form.get('category')
        
        if not name or quantity is None or price is None:
            flash('商品名、数量、価格は必須です', 'error')
            return redirect(url_for('add_item'))
        
        new_item = Item(
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category=category
        )
        
        try:
            db.session.add(new_item)
            db.session.commit()
            flash('商品を追加しました', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('add_item'))
    
    return render_template('add_item.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.quantity = request.form.get('quantity', type=int)
        item.price = request.form.get('price', type=float)
        item.category = request.form.get('category')
        
        if not item.name or item.quantity is None or item.price is None:
            flash('商品名、数量、価格は必須です', 'error')
            return redirect(url_for('edit_item', id=id))
        
        try:
            db.session.commit()
            flash('商品を更新しました', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('edit_item', id=id))
    
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    
    try:
        db.session.delete(item)
        db.session.commit()
        flash('商品を削除しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'エラーが発生しました: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        items = Item.query.filter(
            (Item.name.contains(query)) | 
            (Item.description.contains(query)) | 
            (Item.category.contains(query))
        ).all()
    else:
        items = []
    
    return render_template('search.html', items=items, query=query)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
