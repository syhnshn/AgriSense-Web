{
"system_context": {
"project_name": "AgriSense",
"description": "AI-powered digital agriculture assistant",
"role": "Senior Python Backend Developer",
"tech_stack": ["Python", "PostgreSQL", "SQLAlchemy 2.0", "psycopg2", "Pydantic", "dotenv"]
},
"database_schema": {
"KULLANICI": {"id": "UUID (PK, auto-generated)", "ad_soyad": "String", "email": "String (Unique)", "kayit_tarihi": "DateTime"},
"TARLA": {"id": "Integer (PK)", "kullanici_id": "UUID (FK)", "tarla_adi": "String", "ekin_turu": "String", "ekim_tarihi": "Date", "enlem": "Float", "boylam": "Float"},
"SORU_CEVAP_GECMISI": {"id": "Integer (PK)", "tarla_id": "Integer (FK)", "ciftci_sorusu": "Text", "ai_cevabi": "Text", "islem_tarihi": "DateTime"},
"HAVA_DURUMU_LOG": {"id": "Integer (PK)", "tarla_id": "Integer (FK)", "sicaklik": "Float", "nem": "Float", "risk_durumu": "String", "olcum_tarihi": "DateTime"}
},
"tasks_to_execute": [
{
"task_id": 1,
"description": "Create a database connection module (e.g., `database.py`) using SQLAlchemy. Set up the `engine`, `SessionLocal`, and `Base` declarative class. Use the `DATABASE_URL` from environment variables."
},
{
"task_id": 2,
"description": "Create SQLAlchemy ORM models (e.g., `models.py`) mapping to the provided database schema. Ensure correct relationships (One-to-Many) between KULLANICI -> TARLA, and TARLA -> SORU_CEVAP_GECMISI / HAVA_DURUMU_LOG using `relationship()`."
},
{
"task_id": 3,
"description": "Create Pydantic models (e.g., `schemas.py`) for data validation. Create Base, Create, and Response schemas for each table (e.g., TarlaCreate, TarlaResponse) setting `from_attributes=True` for ORM compatibility."
},
{
"task_id": 4,
"description": "Develop a CRUD operations module (e.g., `crud.py`). Write modular functions to: 1. Create and read a 'Tarla'. 2. Create a 'Hava_Durumu_Log'. 3. Save a 'Soru_Cevap_Gecmisi' entry."
}
],
"output_instructions": {
"language": "Python",
"formatting": "Provide code in clear, separate blocks representing individual files (`database.py`, `models.py`, `schemas.py`, `crud.py`).",
"best_practices": "Ensure clean architecture separation between ORM models and Pydantic schemas.",
"comments": "Add descriptive docstrings and comments in Turkish explaining the logic."
}
}
