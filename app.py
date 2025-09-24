import os
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st

def make_frames(num_frames=180, elev=60, r_axis=0):
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')

    X = np.linspace(-5, 5, 100)
    Y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(X, Y)
    Z = np.exp(-0.1 * (X**2 + Y**2))
    ax.set_axis_off()

    frames = []
    for i in range(num_frames):
        ax.cla()
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        ax.set_axis_off()
        azim = (i * r_axis) % 360
        ax.view_init(elev, azim)

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        im = Image.open(buf).copy()  # 👈 FIXED
        frames.append(im)
        buf.close()

    plt.close(fig)
    return frames


def frames_to_gif(frames, duration=100, loop=0):
    """
    Convert list of PIL Images to a GIF (as bytes).
    """
    buf = BytesIO()
    frames[0].save(
        buf,
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=loop
    )
    buf.seek(0)
    return buf

def main():
    st.title("3D Video / GIF via Python + Matplotlib")
    st.write("This app generates an animated 3D view as a GIF.")
    
    num_frames = st.slider("Number of frames", min_value=36, max_value=360, value=180, step=36)
    elev = st.slider("Elevation angle (degrees)", min_value=0, max_value=90, value=60)
    r_axis = st.slider("Azimuth change per frame (degrees)", min_value=1, max_value=10, value=2)
    duration = st.slider("GIF frame duration (ms)", min_value=20, max_value=200, value=100, step=10)
    
    if st.button("Generate GIF"):
        with st.spinner("Rendering frames..."):
            frames = make_frames(num_frames=num_frames, elev=elev, r_axis=r_axis)
        with st.spinner("Converting to GIF..."):
            gif_bytes = frames_to_gif(frames, duration=duration)
        st.success("Done!")
        st.image(gif_bytes, format="GIF")
        # offer download
        st.download_button(
            label="Download GIF",
            data=gif_bytes,
            file_name="3d_animation.gif",
            mime="image/gif"
        )

if __name__ == "__main__":
    main()
