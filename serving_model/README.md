# Serving Model Output

Folder ini adalah target output komponen TFX `Pusher`.

Setelah pipeline berhasil dijalankan dengan:

```bash
python pipeline.py
```

TFX akan menulis SavedModel yang di-*bless* ke folder ini. Struktur akhirnya harus berisi direktori versi SavedModel (misalnya `1/`) dengan `saved_model.pb` dan folder `variables/`.

File README ini boleh dihapus setelah SavedModel nyata tersedia.
