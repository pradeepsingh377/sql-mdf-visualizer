>import pandas as pd
>import numpy as np
>import matplotlib.pyplot as plt
>
># Load the CSV exported from extract_segments.sql
>df = pd.read_csv("segments.csv")
>
># Group 4MB segments into 16MB blocks (optional clarity for visualization)
>df['block'] = df['segment_id'] // 4
>block_summary = df.groupby('block')['MB_used'].sum().reset_index()
>
># Normalize block usage (0 = empty, 1 = fully used)
>block_summary['normalized'] = block_summary['MB_used'] / 16.0
>
># Build a heatmap matrix (vertical bar)
>width = 60  # heatmap width for LinkedIn clarity
>heat_matrix = np.repeat(block_summary['normalized'].values[:, None], width, axis=1)
>
># Flip so bottom = physical end of MDF file
>heat_matrix = np.flipud(heat_matrix)
>
># Identify the first allocated block in the tail (blocks with >5% used)
>used_blocks = np.where(block_summary['normalized'].values[::-1] > 0.05)[0]
>tail_block = used_blocks[0] if len(used_blocks) else None
>
>plt.figure(figsize=(7, 16))
>plt.imshow(heat_matrix, cmap="bone_r", aspect="auto", origin="lower")
>plt.colorbar(label="Normalized Block Usage (Dark = More Used)")
>
>plt.title("SQL Server MDF Allocation Heatmap", pad=20)
>plt.ylabel("Top = Start of File, Bottom = End of File")
>
>h = heat_matrix.shape[0]
>
># Visualization labels
>plt.text(2, h*0.90, "Mixed Usage Zone", color="white")
>plt.text(2, h*0.60, "Dense Data Zone", color="white")
>plt.text(2, h*0.35, "Mostly Free Space", color="white")
>plt.text(2, h*0.10, "Tail Allocations Blocking SHRINK", color="white")
>
># Draw shrink boundary
>if tail_block is not None:
>    plt.axhline(tail_block, color="red", linestyle="--", linewidth=2)
>    plt.text(58, tail_block + 50, "Shrink Stops Here", color="red", ha='right')
>
>plt.tight_layout()
>plt.savefig("heatmap_example.png", dpi=320)
>plt.show()
