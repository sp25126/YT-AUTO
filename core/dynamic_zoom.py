"""dynamic_zoom.py - FFmpeg dynamic punch-in and zoom filter generator.

Switches between 100% and 115% scale on emphasized moments or every 2.5-3.0s
to satisfy the visual stimulus retention rule.
"""

def generate_zoom_filter(punch_in_intervals: list = None, base_label: str = "fg", output_label: str = "fg_zoomed") -> str:
    """Generates FFmpeg expression for alternating punch-ins."""
    if not punch_in_intervals:
        # Default periodic punch-in: scale alternates between 1.0 and 1.15 every 3 seconds
        expr = "if(mod(t\,6.0)<3.0\,1.0\,1.15)"
    else:
        conditions = []
        for start, end in punch_in_intervals:
            conditions.append(f"between(t\,{start}\,{end})")
        if conditions:
            expr = f"if({'+'.join(conditions)}\,1.15\,1.0)"
        else:
            expr = "1.0"
            
    return f"[{base_label}]scale=eval=frame:w='1080*{expr}':h='-1':flags=bicubic[{output_label}]"

if __name__ == "__main__":
    print(generate_zoom_filter([(2.5, 5.0), (10.0, 13.0)]))
