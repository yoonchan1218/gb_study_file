import zipfile
import os

src_dir = "unpacked_v7"
out_file = "김윤찬_TRY-CATCH_화면_포트폴리오_v7.pptx"

if os.path.exists(out_file):
    os.remove(out_file)

with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            full_path = os.path.join(root, f)
            arcname = os.path.relpath(full_path, src_dir)
            arcname = arcname.replace(os.sep, '/')
            zf.write(full_path, arcname)

size = os.path.getsize(out_file)
print(f"Packed {out_file}: {size:,} bytes")
