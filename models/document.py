from extensions import db
from datetime import datetime

class HRDocument(db.Model):
    __tablename__ = "hr_document"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    chunk_count = db.Column(db.Integer, default=0)
    es_index = db.Column(db.String(100), default="hr_documents")
    status = db.Column(db.String(50), default="processed")

    def to_dict(self):
        return {
            "id" : self.id,
            "filename" : self.filename,
            "uploaded_at" : self.uploaded_at.isoformat(),
            "chunk_count" : self.chunk_count,
            "es_index" : self.es_index,
            "status" : self.status
        }