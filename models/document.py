from extensions import postgres_db
from datetime import datetime

class HRDocument(postgres_db.Model):
    __tablename__ = "hr_document"

    id = postgres_db.Column(postgres_db.Integer, primary_key=True)
    filename = postgres_db.Column(postgres_db.String(255), nullable=False)
    uploaded_at = postgres_db.Column(postgres_db.DateTime, default=datetime.utcnow)
    chunk_count = postgres_db.Column(postgres_db.Integer, default=0)
    es_index = postgres_db.Column(postgres_db.String(100), default="hr_documents")
    status = postgres_db.Column(postgres_db.String(50), default="processed")

    def to_dict(self):
        return {
            "id" : self.id,
            "filename" : self.filename,
            "uploaded_at" : self.uploaded_at.isoformat(),
            "chunk_count" : self.chunk_count,
            "es_index" : self.es_index,
            "status" : self.status
        }