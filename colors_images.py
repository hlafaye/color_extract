import numpy as np
from PIL import Image
from skimage.transform import resize
from sklearn.cluster import KMeans, MiniBatchKMeans
from flask import Flask, render_template, redirect, url_for, flash, request, session, send_file
from  flask_bootstrap import Bootstrap5
import base64
import os 
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()


app = Flask(__name__, static_folder="static", static_url_path="/static")
Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('APP_KEY')

def palette_make(image_path, nb_colors:int):

    def rgb_to_hex(rgb255):
        r, g, b = rgb255
        r = int(np.clip(r, 0, 255))
        g = int(np.clip(g, 0, 255))
        b = int(np.clip(b, 0, 255))
        return f'#{r:02x}{g:02x}{b:02x}'

    img = Image.open(image_path).convert("RGB")
    img.thumbnail((320, 320))
    pixels = np.asarray(img, dtype=np.uint8).reshape(-1, 3)


    kmeans = MiniBatchKMeans(
            n_clusters=nb_colors,
            random_state=0,
            batch_size=2048,
            n_init="auto"
    )
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_
    counts = np.bincount(labels)

    palette = sorted(zip(centers, counts), key=lambda x: x[1], reverse=True)

    return [{"hex": rgb_to_hex(c), "count": int(n)} for c, n in palette]



@app.route('/' ,methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        image_data = request.files.get("file")
        nb_colors = request.form.get("nb_colors", "5")
        try:
            nb_colors = int(nb_colors)
        except ValueError:
            nb_colors = 5
        nb_colors = max(2, min(nb_colors, 12))

        if not image_data or image_data.filename == "":
            return render_template("colors_images.html", error="No image selected")

        raw = image_data.read()  # <-- on lit UNE fois
        image_preview = base64.b64encode(raw).decode("utf-8")

        palette = palette_make(BytesIO(raw), nb_colors=nb_colors)
        return render_template('colors_images.html', palette=palette, image_preview=image_preview)

    return render_template('colors_images.html')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
