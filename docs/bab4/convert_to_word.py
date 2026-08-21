"""
Script untuk mengkonversi Dokumentasi BAB IV ke format Word (.docx)
Lengkap dengan gambar-gambar screenshot
"""

from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

# Path ke folder images
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__), "BAB_IV_Implementasi_dan_Pengujian.docx"
)


def set_document_style(doc):
    """Set default document style"""
    # Set default font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(12)

    # Set paragraph format
    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    paragraph_format.space_after = Pt(0)

    return doc


def add_heading_style(doc, text, level=1):
    """Add styled heading"""
    if level == 1:
        heading = doc.add_heading(text, level=1)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in heading.runs:
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.name = "Times New Roman"
    elif level == 2:
        heading = doc.add_heading(text, level=2)
        for run in heading.runs:
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.name = "Times New Roman"
    elif level == 3:
        heading = doc.add_heading(text, level=3)
        for run in heading.runs:
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.name = "Times New Roman"
    return heading


def add_paragraph(doc, text, indent=True, bold=False):
    """Add paragraph with proper formatting"""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        para.paragraph_format.first_line_indent = Cm(1.27)

    run = para.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.bold = bold

    return para


def add_image_with_caption(doc, image_path, caption, width=5.5):
    """Add image with centered caption"""
    if os.path.exists(image_path):
        # Add image
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run()
        run.add_picture(image_path, width=Inches(width))

        # Add caption
        caption_para = doc.add_paragraph()
        caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption_run = caption_para.add_run(caption)
        caption_run.font.name = "Times New Roman"
        caption_run.font.size = Pt(10)
        caption_run.italic = True

        # Add space after
        doc.add_paragraph()
    else:
        # Placeholder if image not found
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(f"[Gambar tidak ditemukan: {os.path.basename(image_path)}]")
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.italic = True

        caption_para = doc.add_paragraph()
        caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption_run = caption_para.add_run(caption)
        caption_run.font.name = "Times New Roman"
        caption_run.font.size = Pt(10)
        caption_run.italic = True


def add_bullet_list(doc, items):
    """Add bullet list"""
    for item in items:
        para = doc.add_paragraph(style="List Bullet")
        run = para.add_run(item)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)


def add_numbered_list(doc, items):
    """Add numbered list"""
    for item in items:
        para = doc.add_paragraph(style="List Number")
        run = para.add_run(item)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)


def add_table(doc, headers, rows):
    """Add formatted table"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header
        for para in header_cells[i].paragraphs:
            for run in para.runs:
                run.font.bold = True
                run.font.name = "Times New Roman"
                run.font.size = Pt(11)

    # Data rows
    for row_idx, row_data in enumerate(rows):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_data in enumerate(row_data):
            row_cells[col_idx].text = str(cell_data)
            for para in row_cells[col_idx].paragraphs:
                for run in para.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(11)

    doc.add_paragraph()  # Space after table
    return table


def create_bab4_document():
    """Create BAB IV document"""
    doc = Document()
    doc = set_document_style(doc)

    # ==================== BAB IV TITLE ====================
    add_heading_style(doc, "BAB IV", 1)
    add_heading_style(doc, "IMPLEMENTASI DAN PENGUJIAN", 1)
    doc.add_paragraph()

    # ==================== 4.1 Lingkungan Pengembangan ====================
    add_heading_style(doc, "4.1 Lingkungan Pengembangan", 2)

    add_paragraph(
        doc,
        "Pada bagian ini akan dijelaskan mengenai lingkungan pengembangan yang digunakan dalam membangun sistem pencarian jurnal penelitian menggunakan metode Content-Based Filtering.",
    )

    # 4.1.1
    add_heading_style(doc, "4.1.1 Perangkat Keras", 3)
    add_paragraph(
        doc,
        "Spesifikasi perangkat keras yang digunakan dalam pengembangan sistem adalah sebagai berikut:",
    )
    add_bullet_list(
        doc,
        [
            "Processor: Intel Core i5 / AMD Ryzen 5 atau setara",
            "RAM: 8 GB DDR4",
            "Storage: SSD 256 GB",
            "Display: 1920 x 1080 pixels",
        ],
    )

    # 4.1.2
    add_heading_style(doc, "4.1.2 Perangkat Lunak", 3)
    add_paragraph(
        doc, "Perangkat lunak yang digunakan dalam pengembangan sistem meliputi:"
    )
    add_bullet_list(
        doc,
        [
            "Sistem Operasi: Windows 10/11",
            "Python 3.9+",
            "Flask Framework 2.0+",
            "Visual Studio Code",
            "Browser: Google Chrome / Mozilla Firefox",
        ],
    )

    # 4.1.3
    add_heading_style(doc, "4.1.3 Library dan Framework", 3)
    add_paragraph(doc, "Library Python yang digunakan dalam implementasi sistem:")

    add_table(
        doc,
        ["Library", "Versi", "Fungsi"],
        [
            ["Flask", "2.0+", "Web framework untuk backend"],
            ["scikit-learn", "1.0+", "Implementasi TF-IDF dan Cosine Similarity"],
            ["NLTK", "3.6+", "Natural Language Processing"],
            ["numpy", "1.21+", "Operasi numerik dan array"],
            ["requests", "2.26+", "HTTP requests ke API eksternal"],
        ],
    )

    # ==================== 4.2 Implementasi Sistem ====================
    add_heading_style(doc, "4.2 Implementasi Sistem", 2)

    add_paragraph(
        doc,
        "Implementasi sistem pencarian jurnal penelitian ini terdiri dari beberapa komponen utama yang saling terintegrasi untuk menghasilkan rekomendasi jurnal yang relevan berdasarkan query pengguna.",
    )

    # 4.2.1
    add_heading_style(doc, "4.2.1 Arsitektur Sistem", 3)
    add_paragraph(
        doc,
        "Sistem dibangun dengan arsitektur client-server menggunakan Flask sebagai backend dan HTML/CSS/JavaScript sebagai frontend. Berikut adalah alur kerja sistem:",
    )

    add_numbered_list(
        doc,
        [
            "User memasukkan query pencarian",
            "Sistem mengambil data dari API (CrossRef/Semantic Scholar)",
            "Proses preprocessing teks dilakukan",
            "Perhitungan TF-IDF untuk setiap dokumen",
            "Perhitungan Cosine Similarity antara query dan dokumen",
            "Hasil diranking berdasarkan nilai similarity tertinggi",
            "Tampilkan hasil ke pengguna",
        ],
    )

    # 4.2.2
    add_heading_style(doc, "4.2.2 Implementasi Content-Based Filtering", 3)
    add_paragraph(
        doc,
        "Content-Based Filtering diimplementasikan dengan menggunakan kombinasi TF-IDF (Term Frequency - Inverse Document Frequency) dan Cosine Similarity. Metode ini menganalisis konten dari jurnal (judul dan abstrak) untuk menentukan relevansi dengan query pengguna.",
    )

    add_paragraph(doc, "Rumus TF-IDF yang digunakan adalah:", indent=False)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run("TF-IDF(t,d) = TF(t,d) × IDF(t)")
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.bold = True

    add_paragraph(
        doc,
        "Dimana TF = frekuensi term dalam dokumen, IDF = log(N/df) + 1",
        indent=False,
    )

    add_paragraph(doc, "Rumus Cosine Similarity yang digunakan adalah:", indent=False)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run("cos(θ) = (A · B) / (||A|| × ||B||)")
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.bold = True

    add_paragraph(
        doc,
        "Rumus ini mengukur kemiripan berdasarkan sudut antara dua vektor dalam ruang TF-IDF.",
        indent=False,
    )

    # ==================== 4.3 Antarmuka Sistem ====================
    add_heading_style(doc, "4.3 Antarmuka Sistem", 2)

    add_paragraph(
        doc,
        "Pada bagian ini akan ditampilkan antarmuka sistem yang telah diimplementasikan beserta penjelasan fungsi dari masing-masing komponen.",
    )

    # 4.3.1 Halaman Pencarian
    add_heading_style(doc, "4.3.1 Halaman Pencarian Utama", 3)
    add_paragraph(
        doc,
        "Halaman utama sistem menampilkan form pencarian dimana pengguna dapat memasukkan kata kunci untuk mencari jurnal penelitian yang relevan. Sistem menyediakan berbagai filter untuk mempersempit hasil pencarian.",
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "01_homepage.png"),
        "Gambar 4.1 Tampilan Halaman Pencarian Utama Sistem",
    )

    add_paragraph(
        doc,
        "Berdasarkan Gambar 4.1, halaman pencarian utama terdiri dari beberapa komponen:",
    )
    add_numbered_list(
        doc,
        [
            "Search Box: Input field untuk memasukkan kata kunci pencarian",
            "Filter Options: Opsi untuk memfilter berdasarkan tahun, sumber data, dan jumlah hasil",
            "Search Button: Tombol untuk menjalankan proses pencarian",
        ],
    )

    # 4.3.2 Navigasi Proses CBF
    add_heading_style(doc, "4.3.2 Navigasi Proses Content-Based Filtering", 3)
    add_paragraph(
        doc,
        "Setelah proses pencarian selesai, sistem menampilkan navigasi 4 tahap proses Content-Based Filtering. Pengguna dapat mengklik setiap tab untuk melihat detail dari masing-masing tahap perhitungan.",
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "03_search_results.png"),
        "Gambar 4.2 Navigasi 4 Tahap Proses Content-Based Filtering",
    )

    add_paragraph(doc, "Navigasi proses CBF terdiri dari 4 tahap utama:")
    add_numbered_list(
        doc,
        [
            "Preprocessing: Tahap pembersihan dan normalisasi teks",
            "TF-IDF: Tahap perhitungan bobot term",
            "Cosine Similarity: Tahap perhitungan kemiripan",
            "Ranking: Tahap pemeringkatan hasil akhir",
        ],
    )

    # 4.3.3 Text Preprocessing
    add_heading_style(doc, "4.3.3 Tahap 1: Text Preprocessing", 3)
    add_paragraph(
        doc,
        "Tahap pertama dalam proses Content-Based Filtering adalah preprocessing teks. Pada tahap ini, teks dari query dan dokumen jurnal dibersihkan dan dinormalisasi agar dapat diproses lebih lanjut.",
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "03_preprocessing.png"),
        "Gambar 4.3 Visualisasi Tahap Preprocessing Teks",
    )

    add_paragraph(doc, "Proses preprocessing teks terdiri dari 4 langkah utama:")
    add_numbered_list(
        doc,
        [
            "Case Folding (lowercase) - Mengubah semua huruf menjadi huruf kecil",
            "Tokenisasi - Memecah teks menjadi kata-kata individual",
            "Penghapusan Stopwords - Menghapus kata umum (the, is, a, an, dll)",
            "Lemmatisasi - Mengubah kata ke bentuk dasar (running → run)",
        ],
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "04_tfidf_matrix.png"),
        "Gambar 4.4 Contoh Hasil Preprocessing Query dan Dokumen",
    )

    add_paragraph(
        doc,
        'Gambar 4.4 menunjukkan contoh hasil preprocessing dimana query asli "penjadwalan genetika untuk mahasiswa" diubah menjadi "penjadwalan genetika mahasiswa" setelah melalui proses preprocessing. Tabel juga menampilkan perbandingan teks original dengan teks setelah preprocessing untuk setiap dokumen jurnal.',
    )

    # 4.3.4 TF-IDF Calculation
    add_heading_style(doc, "4.3.4 Tahap 2: Perhitungan TF-IDF", 3)
    add_paragraph(
        doc,
        "Tahap kedua adalah perhitungan TF-IDF (Term Frequency - Inverse Document Frequency). Metode ini memberikan bobot pada setiap term berdasarkan frekuensi kemunculannya dalam dokumen dan keunikannya di seluruh koleksi dokumen.",
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "05_tfidf_details.png"),
        "Gambar 4.5 Visualisasi Perhitungan TF-IDF dengan Matrix",
    )

    add_paragraph(doc, "Berdasarkan Gambar 4.5, sistem menampilkan:")
    add_bullet_list(
        doc,
        [
            "Rumus TF-IDF: Formula matematika yang digunakan dalam perhitungan",
            "Total Terms Unik: 1008 term unik ditemukan dari seluruh dokumen",
            "Total Dokumen: 10 dokumen jurnal yang dianalisis",
            "Matrix TF-IDF: Tabel yang menunjukkan nilai TF-IDF untuk setiap kombinasi dokumen dan term",
        ],
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "11_detail_preprocessing_dark.png"),
        "Gambar 4.6 Detail Perhitungan TF-IDF per Term",
    )

    add_paragraph(
        doc,
        "Gambar 4.6 menampilkan detail perhitungan TF-IDF untuk setiap term teratas, meliputi:",
    )
    add_bullet_list(
        doc,
        [
            "Term: Kata yang dianalisis",
            "DF (Document Frequency): Jumlah dokumen yang mengandung term tersebut",
            "IDF Calculation: Perhitungan IDF dengan rumus log(N/df) + 1",
            "Avg TF-IDF: Rata-rata nilai TF-IDF untuk term tersebut",
        ],
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "12_top_terms.png"),
        "Gambar 4.7 Top TF-IDF Terms untuk Setiap Dokumen",
    )

    add_paragraph(
        doc,
        "Gambar 4.7 menunjukkan term-term dengan nilai TF-IDF tertinggi untuk setiap dokumen (D1-D10). Visualisasi ini membantu memahami kata kunci penting yang menjadi karakteristik setiap jurnal.",
    )

    # 4.3.5 Cosine Similarity
    add_heading_style(doc, "4.3.5 Tahap 3: Perhitungan Cosine Similarity", 3)
    add_paragraph(
        doc,
        "Tahap ketiga adalah perhitungan Cosine Similarity yang mengukur tingkat kemiripan antara query pengguna dengan setiap dokumen jurnal berdasarkan sudut antara vektor TF-IDF mereka.",
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "06-cosine.png"),
        "Gambar 4.8 Visualisasi Perhitungan Cosine Similarity",
    )

    add_paragraph(doc, "Berdasarkan Gambar 4.8, sistem menampilkan:")
    add_bullet_list(
        doc,
        [
            "Rumus Cosine Similarity: Formula (A · B) / (||A|| × ||B||)",
            "Query Information: Query asli dan hasil preprocessing",
            "Tabel Similarity: Nilai similarity untuk setiap dokumen terhadap query",
        ],
    )

    add_paragraph(doc, "Kategori relevansi berdasarkan nilai Cosine Similarity:")
    add_bullet_list(
        doc,
        [
            "≥ 70% - Sangat Relevan",
            "40% - 70% - Cukup Relevan",
            "< 40% - Kurang Relevan",
        ],
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "08_cosine_table.png"),
        "Gambar 4.9 Detail Perhitungan Cosine Similarity per Dokumen",
    )

    add_paragraph(
        doc,
        'Gambar 4.9 menampilkan detail perhitungan dengan kolom Calculation yang menunjukkan nilai dot product, magnitude, dan hasil akhir similarity. Dari hasil pencarian dengan query "penjadwalan genetika untuk mahasiswa", diperoleh:',
    )
    add_bullet_list(
        doc,
        [
            "D1: Algoritma Genetika untuk Sistem Penjadwalan... - Similarity: 12.17%",
            "D2: Implementasi Algoritma Genetika Untuk Op... - Similarity: 8.05%",
            "D3-D10: Dokumen lainnya dengan similarity 0%",
        ],
    )

    # 4.3.6 Final Ranking
    add_heading_style(doc, "4.3.6 Tahap 4: Hasil Ranking Akhir", 3)
    add_paragraph(
        doc,
        "Tahap terakhir adalah pemeringkatan hasil berdasarkan nilai Cosine Similarity. Jurnal dengan nilai similarity tertinggi akan ditampilkan di posisi teratas sebagai rekomendasi utama.",
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "07-ranking.png"),
        "Gambar 4.10 Hasil Ranking Akhir Jurnal",
    )

    add_paragraph(doc, "Berdasarkan Gambar 4.10, hasil ranking menampilkan:")
    add_bullet_list(
        doc,
        [
            "Rata-rata Relevansi: 2.14% - menunjukkan rata-rata similarity seluruh dokumen",
            "Relevansi Tertinggi: 12.85% - nilai similarity tertinggi yang dicapai",
            "Daftar Ranking: Tabel jurnal yang diurutkan berdasarkan skor relevansi",
        ],
    )

    add_paragraph(doc, "Dari hasil ranking, jurnal dengan peringkat tertinggi adalah:")
    add_numbered_list(
        doc,
        [
            'Rank 1: "Algoritma Genetika untuk Sistem Penjadwalan Perkuliahan Menggunakan Multiple Random Crossover" (2020) - 12.85%',
            'Rank 2: "Implementasi Algoritma Genetika Untuk Optimasi Penjadwalan Mata Kuliah" (2018) - 8.57%',
            'Rank 3: "PENERAPAN ALGORITMA GENETIKA UNTUK PENJADWALAN MATA PELAJARAN" (2024) - 0.00%',
        ],
    )

    # 4.3.7 Tab Detail Perhitungan
    add_heading_style(doc, "4.3.7 Tab Detail Perhitungan", 3)
    add_paragraph(
        doc,
        'Selain tab proses CBF, sistem juga menyediakan tab "Detail Perhitungan" yang menampilkan informasi lebih lengkap tentang seluruh proses perhitungan dalam satu tampilan terintegrasi.',
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "13_cosine_detail_dark.png"),
        "Gambar 4.11 Tab Detail Perhitungan dengan Tampilan Terintegrasi",
    )

    add_paragraph(doc, "Tab Detail Perhitungan menampilkan:")
    add_numbered_list(
        doc,
        [
            "Tahap 1: Preprocessing Teks - Ringkasan proses preprocessing",
            "Tahap 2: Pembobotan TF-IDF - Tabel detail perhitungan per term",
            "Tahap 3: Cosine Similarity - Matrix similarity dan statistik",
            "Top TF-IDF Terms per Dokumen - Kata kunci penting setiap jurnal",
        ],
    )

    add_image_with_caption(
        doc,
        os.path.join(IMAGES_DIR, "10_final_ranking.png"),
        "Gambar 4.12 Statistik Hasil Analisis CBF",
    )

    add_paragraph(doc, "Statistik hasil menampilkan ringkasan perhitungan:")
    add_bullet_list(
        doc,
        [
            "Dokumen Dianalisis: 10 jurnal",
            "Total Terms Unik: 1008 kata unik",
            "Rata-rata Relevansi: 2.14%",
            "Relevansi Tertinggi: 12.85%",
        ],
    )

    # ==================== 4.4 Pengujian Sistem ====================
    add_heading_style(doc, "4.4 Pengujian Sistem", 2)

    # 4.4.1
    add_heading_style(doc, "4.4.1 Pengujian Fungsional", 3)
    add_paragraph(
        doc,
        "Pengujian fungsional dilakukan untuk memastikan semua fitur sistem berjalan dengan baik sesuai spesifikasi.",
    )

    add_table(
        doc,
        ["No", "Fitur", "Skenario Pengujian", "Hasil"],
        [
            [
                "1",
                "Pencarian Jurnal",
                "Memasukkan query dan menekan tombol search",
                "Berhasil",
            ],
            [
                "2",
                "Filter Tahun",
                "Memfilter hasil berdasarkan rentang tahun",
                "Berhasil",
            ],
            [
                "3",
                "Visualisasi Preprocessing",
                "Menampilkan tahap preprocessing dengan benar",
                "Berhasil",
            ],
            [
                "4",
                "Matrix TF-IDF",
                "Menampilkan matrix TF-IDF dokumen x term",
                "Berhasil",
            ],
            [
                "5",
                "Cosine Similarity",
                "Menghitung dan menampilkan nilai similarity",
                "Berhasil",
            ],
            [
                "6",
                "Ranking Hasil",
                "Mengurutkan hasil berdasarkan relevansi",
                "Berhasil",
            ],
            [
                "7",
                "Tab Navigation",
                "Perpindahan antar tab berfungsi dengan baik",
                "Berhasil",
            ],
        ],
    )

    # 4.4.2
    add_heading_style(doc, "4.4.2 Pengujian Akurasi Content-Based Filtering", 3)
    add_paragraph(
        doc,
        "Pengujian akurasi dilakukan dengan membandingkan hasil rekomendasi sistem dengan penilaian manual berdasarkan relevansi query dengan konten jurnal.",
    )

    add_table(
        doc,
        ["Query", "Top 3 Hasil", "Similarity", "Relevansi Manual"],
        [
            [
                "penjadwalan genetika untuk mahasiswa",
                "Algoritma Genetika untuk Sistem Penjadwalan...",
                "12.85%",
                "Relevan",
            ],
            [
                "",
                "Implementasi Algoritma Genetika Untuk Optimasi...",
                "8.57%",
                "Relevan",
            ],
            [
                "",
                "PENERAPAN ALGORITMA GENETIKA UNTUK PENJADWALAN...",
                "0.00%",
                "Cukup Relevan",
            ],
        ],
    )

    # ==================== 4.5 Analisis Hasil ====================
    add_heading_style(doc, "4.5 Analisis Hasil", 2)

    # 4.5.1
    add_heading_style(doc, "4.5.1 Analisis Hasil Pencarian", 3)
    add_paragraph(
        doc,
        "Berdasarkan pengujian yang telah dilakukan, sistem pencarian jurnal menggunakan Content-Based Filtering dengan metode TF-IDF dan Cosine Similarity berhasil memberikan rekomendasi jurnal yang relevan dengan query pengguna.",
    )

    # 4.5.2
    add_heading_style(doc, "4.5.2 Analisis Relevansi Ranking", 3)
    add_paragraph(
        doc,
        'Dari hasil pengujian dengan query "penjadwalan genetika untuk mahasiswa", jurnal dengan relevansi tertinggi (12.85%) memang membahas topik yang sangat sesuai yaitu tentang algoritma genetika untuk sistem penjadwalan perkuliahan. Hal ini menunjukkan bahwa metode Content-Based Filtering dapat mengidentifikasi konten yang relevan dengan baik.',
    )

    add_paragraph(
        doc,
        "Nilai similarity yang relatif rendah (rata-rata 2.14%) menunjukkan bahwa query pengguna perlu lebih spesifik untuk mendapatkan hasil yang lebih relevan. Jurnal dengan similarity di atas 10% dapat dianggap sebagai rekomendasi yang layak.",
    )

    # 4.5.3
    add_heading_style(doc, "4.5.3 Analisis Perhitungan TF-IDF dan Cosine Similarity", 3)
    add_paragraph(
        doc,
        "Visualisasi Matrix TF-IDF membantu pengguna memahami bagaimana sistem memberikan bobot pada setiap term. Term dengan nilai TF-IDF tinggi menunjukkan kata kunci yang penting dan unik untuk dokumen tersebut.",
    )

    add_paragraph(
        doc,
        "Perhitungan Cosine Similarity yang ditampilkan secara transparan memungkinkan pengguna untuk memverifikasi dan memahami bagaimana sistem menentukan tingkat kemiripan antara query dan dokumen.",
    )

    # Kesimpulan
    add_paragraph(doc, "Kesimpulan BAB IV:", bold=True, indent=False)
    add_paragraph(
        doc,
        "Sistem pencarian jurnal penelitian menggunakan Content-Based Filtering telah berhasil diimplementasikan dengan fitur-fitur utama:",
    )
    add_bullet_list(
        doc,
        [
            "Pencarian jurnal dari multiple API (CrossRef, Semantic Scholar)",
            "Visualisasi lengkap 4 tahap proses CBF",
            "Matrix TF-IDF interaktif",
            "Perhitungan Cosine Similarity transparan",
            "Ranking hasil berdasarkan relevansi",
        ],
    )

    add_paragraph(
        doc,
        "Pengujian menunjukkan bahwa sistem berfungsi dengan baik dan dapat memberikan rekomendasi jurnal yang relevan berdasarkan query pengguna.",
    )

    # Save document
    doc.save(OUTPUT_FILE)
    print(f"[OK] Dokumen berhasil dibuat: {OUTPUT_FILE}")
    return OUTPUT_FILE


if __name__ == "__main__":
    print("=" * 50)
    print("Konversi Dokumentasi BAB IV ke Word")
    print("=" * 50)

    # Check if python-docx is installed
    try:
        from docx import Document

        print("[OK] Library python-docx tersedia")
    except ImportError:
        print("[ERROR] Library python-docx belum terinstall")
        print("   Jalankan: pip install python-docx")
        exit(1)

    # Check images
    print("\n[INFO] Memeriksa gambar...")
    images = [
        "01_homepage.png",
        "03_search_results.png",
        "03_preprocessing.png",
        "04_tfidf_matrix.png",
        "05_tfidf_details.png",
        "06-cosine.png",
        "07-ranking.png",
        "08_cosine_table.png",
        "10_final_ranking.png",
        "11_detail_preprocessing_dark.png",
        "12_top_terms.png",
        "13_cosine_detail_dark.png",
    ]

    for img in images:
        path = os.path.join(IMAGES_DIR, img)
        if os.path.exists(path):
            print(f"   [OK] {img}")
        else:
            print(f"   [WARN] {img} - tidak ditemukan")

    # Create document
    print("\n[INFO] Membuat dokumen Word...")
    output = create_bab4_document()

    print("\n" + "=" * 50)
    print(f"[DONE] File tersimpan di: {output}")
    print("=" * 50)
