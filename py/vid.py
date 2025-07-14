import matrix_viz
import matrix_version

import imageio.v3 as iio
import numpy as np
import os


def make_video_from_images_v3(image_dir: str, output_filename: str, fps: int = 3):
    files = sorted(
        [
            f
            for f in os.listdir(image_dir)
            if f.startswith("matrix_viz-") and f.endswith(".png")
        ]
    )

    # Full file paths
    image_paths = [os.path.join(image_dir, f) for f in files]

    # Open MP4 writer
    with iio.imopen(output_filename, "w", plugin="pyav") as writer:
        writer.init_video_stream("libx264", fps=fps)

        for path in image_paths:
            frame = iio.imread(path)

            # Drop alpha channel if present
            if frame.shape[-1] == 4:
                frame = frame[:, :, :3]

            writer.write_frame(frame)


if __name__ == "__main__":
    # for i in range(17, 65536):
    # for i in range(17, 65536, 33):
    #     mg = matrix_version.MatrixGraph(i)
    #     dim = len(mg.to_matrix())
    #     print(
    #         f"n={i}, dim={dim}, entries={[ (e[0].to_int(), e[1].to_int()) for e in mg.entries ]}"
    #     )
    #     mg_int = mg.to_int()
    #     assert mg.to_int() == i, f"mg_int for {i} is {mg.to_int()}"
    #     matrix_viz.visualize_matrixgraph_colored_blended(
    #         mg, f"matrix_viz-{str(i).zfill(5)}"
    #     )

    make_video_from_images_v3("./py/artifacts", "matrix_graphs.mp4", fps=2)
