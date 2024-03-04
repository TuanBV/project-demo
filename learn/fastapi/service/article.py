from sqlalchemy.orm.session import Session
from schemas.article import ArticleRequest
from models.article import Article

# Create article
def create(db: Session, request: ArticleRequest):
    new_article = Article(
        title = request.title,
        content = request.content,
        published = request.published,
        user_id = request.creator_id,
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

# Get article
def get_all_article(db: Session):
    return db.query(Article).all()

