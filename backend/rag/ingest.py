import chromadb
from chromadb.config import Settings
from pathlib import Path

CHROMA_PATH = Path(__file__).resolve().parent / "chroma_store"

career_docs = [
    {"id": "1", "text": "A Software Engineer transitioning to a Data Scientist role should focus on learning Python, statistics, machine learning fundamentals, and tools like Pandas, Scikit-learn, and TensorFlow. Building 2-3 end-to-end ML projects is essential."},
    {"id": "2", "text": "Senior developers moving into engineering management should develop skills in team leadership, project planning, stakeholder communication, and agile methodologies. Reading books like 'The Manager's Path' is recommended."},
    {"id": "3", "text": "A Backend Engineer wanting to become a Full Stack Engineer should learn React or Vue.js, CSS frameworks like Tailwind, and understand REST API consumption from the frontend perspective."},
    {"id": "4", "text": "IT professionals transitioning to Product Management need to develop skills in user research, product roadmapping, writing PRDs, and tools like Jira, Figma, and Mixpanel."},
    {"id": "5", "text": "A DevOps Engineer looking to specialize in Cloud Architecture should pursue AWS/GCP/Azure certifications, learn Terraform for infrastructure as code, and study distributed systems design."},
    {"id": "6", "text": "Professionals with 10+ years of experience in software development can transition into solution architecture by deepening system design knowledge, cloud expertise, and client-facing communication skills."},
    {"id": "7", "text": "A QA Engineer moving into SDET (Software Development Engineer in Test) role should learn test automation frameworks like Selenium, Cypress, or Playwright, and understand CI/CD pipelines."},
    {"id": "8", "text": "Data Analysts wanting to become Data Engineers should learn SQL at an advanced level, pick up Apache Spark, Airflow for pipeline orchestration, and cloud data warehouses like BigQuery or Snowflake."},
    {"id": "9", "text": "Frontend Engineers transitioning to UI/UX Design should study design principles, learn Figma, understand user research methodologies, and build a portfolio of redesign case studies."},
    {"id": "10", "text": "Cybersecurity professionals can advance by obtaining certifications like CISSP, CEH, or OSCP, specializing in penetration testing, cloud security, or incident response."},
]

def ingest():
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name="career_knowledge")

    existing = collection.get()
    existing_ids = set(existing["ids"])

    new_docs = [d for d in career_docs if d["id"] not in existing_ids]
    if not new_docs:
        print("ChromaDB already up to date.")
        return

    collection.add(
        documents=[d["text"] for d in new_docs],
        ids=[d["id"] for d in new_docs],
    )
    print(f"Ingested {len(new_docs)} documents into ChromaDB.")

if __name__ == "__main__":
    ingest()