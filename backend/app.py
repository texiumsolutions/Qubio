from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge
from backend.config import Config
from backend.celery_worker import make_celery

from backend.routes.antifold import antifold_bp
from backend.routes.protein_mpnn import proteinmpnn_bp
from backend.routes.tasks import tasks_bp
from backend.routes.ligand_mpnn import ligandmpnn_bp
from backend.routes.thompson_sampling import ts_bp
from backend.routes.freewilson import freewilson_bp
from backend.routes.colabdock import colabdock_bp
from backend.routes.reinvent import reinvent_bp
from backend.routes.parasurf import parasurf_bp
from backend.routes.thermompnn import thermompnn_bp
from backend.routes.admet_ai import admet_bp
from backend.routes.localcolabfold import localcolabfold_bp

app = Flask(__name__)
app.config.from_object(Config)

# Set max file upload size to 100MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

CORS(app)
celery = make_celery(app)

# Handle large file error with custom response
@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return jsonify({"error": "Uploaded file is too large. Limit is 100MB."}), 413

# Register blueprints
app.register_blueprint(antifold_bp, url_prefix="/v1/api/antifold")
app.register_blueprint(proteinmpnn_bp, url_prefix="/v1/api/proteinmpnn")
app.register_blueprint(tasks_bp, url_prefix="/v1/api/tasks")
app.register_blueprint(ligandmpnn_bp, url_prefix="/v1/api/ligandmpnn")
app.register_blueprint(ts_bp, url_prefix="/v1/api/thompson_sampling")
app.register_blueprint(freewilson_bp, url_prefix="/v1/api/freewilson")
app.register_blueprint(colabdock_bp, url_prefix="/v1/api/colabdock")
app.register_blueprint(reinvent_bp, url_prefix="/v1/api/reinvent")
app.register_blueprint(parasurf_bp, url_prefix="/v1/api/parasurf")
app.register_blueprint(thermompnn_bp, url_prefix="/v1/api/thermompnn")
app.register_blueprint(admet_bp, url_prefix="/v1/api/admet")
app.register_blueprint(localcolabfold_bp, url_prefix="/v1/api/localcolabfold")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

