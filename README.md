#drop in readme contents
# PT Compliance Platform (cross platform starter)

A proof of concept system that lets physical therapists (PTs) record **baseline movements** and lets patients **compare** their own movements in real time using only commodity apple devices.

##Core idea
* PT records “gold standard” set of reps.
* Patient app streams accelerometer /gyro data.
* Backend scores similarity and returns instant feedback.

##Tech stack
| Layer | Tech |
| Mobile / Wear OS | **Flutter** (`sensors_plus`, `sqflite`) |
| Backend API | **FastAPI** + Pydantic |
| Web dashboard | **Next.js** + Chakra UI |
| CI / CD | GitHub Actions → debug APK + Docker image |
| Storage | SQLite local, Postgres cloud (via SQLAlchemy) |
