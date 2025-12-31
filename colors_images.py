import numpy as np
from PIL import Image
from skimage.transform import resize
from sklearn.cluster import KMeans
from flask import Flask, render_template, redirect, url_for, flash, request, session, send_file
from  flask_bootstrap import Bootstrap5
import base64
import os 
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, static_folder="static", static_url_path="/static")
Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('APP_KEY')

def palette_make(image_path, nb_colors:int):

    def rgb_to_hex(rgb):
        r, g, b = rgb
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)
    resized_image = resize(pixels, (320, 320), anti_aliasing=True)

    array_2d = resized_image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=nb_colors, random_state=0, n_init="auto").fit(array_2d)
    colors = kmeans.cluster_centers_

    labels = kmeans.labels_
    counts = np.bincount(labels)

    palette = sorted(zip(colors, counts),key=lambda x: x[1],reverse=True)

    colors_palette = []

    for color, count in palette:
        colors_palette.append({
            "hex": rgb_to_hex(color),
            "count": int(count)
        })
    return colors_palette



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
        encoded_bytes = base64.b64encode(image_data.read())
        image_data.seek(0)  
        image_preview = encoded_bytes.decode("utf-8")

        palette=palette_make(image_path=image_data, nb_colors=nb_colors)
        return render_template('colors_images.html', palette=palette, image_preview=image_preview)

    return render_template('colors_images.html')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
