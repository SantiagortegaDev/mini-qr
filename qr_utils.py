import qrcode

def qr_ascii_half_block(uri: str, background: bool) -> str:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=2,
    )
    qr.add_data(uri)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    if len(matrix[0]) > 41:
        return "too long"

    lines = []
    for r in range(0, len(matrix), 2):
        top_row = matrix[r]
        bottom_row = matrix[r + 1] if r + 1 < len(matrix) else [False] * len(top_row)
        line = []
        for top, bottom in zip(top_row, bottom_row):
            if top and bottom:
                if background:
                 line.append(" ")
                else:
                     line.append("█")
            elif top:
                if background:

                 line.append("▄")
                else:
                     line.append("▀")
            elif bottom:
                if background:
                 line.append("▀")
                else:
                   line.append("▄")
            else:
                if background:
                 line.append("█")
                else:
                    line.append(" ")
        lines.append("".join(line))
    return "\n".join(lines)