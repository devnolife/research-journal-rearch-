"""
Content-Based Filtering Module
Menggunakan TF-IDF dan Cosine Similarity untuk rekomendasi jurnal

Alur:
1. Input (Kata kunci/Query)
2. Preprocessing Teks
3. Pembobotan TF-IDF
4. Perhitungan Cosine Similarity
5. Ranking & Rekomendasi
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class ContentBasedFilter:
    """
    Content-Based Filtering menggunakan TF-IDF dan Cosine Similarity
    """
    
    def __init__(self):
        # TF-IDF dengan parameter yang lebih permissive untuk menghindari pruning error
        self.vectorizer = None  # Will be created dynamically based on corpus size
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

        # Stopwords bahasa Inggris yang lebih lengkap
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()

        # Tambahkan stopwords bahasa Indonesia juga
        try:
            self.stop_words.update(stopwords.words('indonesian'))
        except:
            pass

        # Tambahan stopwords umum yang sering muncul (Inggris)
        common_stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'we', 'this', 'which', 'can', 'have',
            'been', 'had', 'were', 'their', 'they', 'our', 'may', 'also',
            'these', 'those', 'than', 'such', 'into', 'through', 'more',
            'over', 'both', 'between', 'during', 'before', 'after', 'above',
            'below', 'up', 'down', 'out', 'off', 'again', 'further', 'then'
        }

        # Tambahan stopwords bahasa Indonesia yang umum
        indonesian_stopwords = {
            'ada', 'adalah', 'adanya', 'adapun', 'agak', 'agaknya', 'agar',
            'akan', 'akankah', 'akhir', 'akhiri', 'akhirnya', 'aku', 'akulah',
            'amat', 'amatlah', 'anda', 'andalah', 'antar', 'antara', 'antaranya',
            'apa', 'apaan', 'apabila', 'apakah', 'apalagi', 'apatah', 'artinya',
            'asal', 'asalkan', 'atas', 'atau', 'ataukah', 'ataupun', 'awal',
            'awalnya', 'bagai', 'bagaikan', 'bagaimana', 'bagaimanapun', 'bagaimanakah',
            'bagi', 'bagian', 'bahkan', 'bahwa', 'bahwasanya', 'baik', 'bakal',
            'bakalan', 'balik', 'banyak', 'banyaknya', 'bapak', 'baru', 'bawah',
            'beberapa', 'begini', 'beginian', 'beginikah', 'beginilah', 'begitu',
            'begitukah', 'begitulah', 'begitupun', 'bekerja', 'belakang', 'belakangan',
            'belum', 'belumlah', 'benar', 'benarkah', 'benarlah', 'berada', 'berakhir',
            'berakhirlah', 'berakhirnya', 'berapa', 'berapakah', 'berapalah', 'berapapun',
            'berarti', 'berawal', 'berbagai', 'berdatangan', 'beri', 'berikan', 'berikut',
            'berikutnya', 'berjumlah', 'berkali', 'berkata', 'berkehendak', 'berkeinginan',
            'berkenaan', 'berlainan', 'berlalu', 'berlangsung', 'berlebihan', 'bermacam',
            'bermaksud', 'bermula', 'bersama', 'bersiap', 'bersiap-siap', 'bertanya',
            'bertanya-tanya', 'berturut', 'berturut-turut', 'bertutur', 'berujar',
            'berupa', 'besar', 'betul', 'betulkah', 'biasa', 'biasanya', 'bila',
            'bilakah', 'bisa', 'bisakah', 'boleh', 'bolehkah', 'bolehlah', 'buat',
            'bukan', 'bukankah', 'bukanlah', 'bukannya', 'bulan', 'bung', 'cara',
            'caranya', 'cukup', 'cukupkah', 'cukuplah', 'cuma', 'dahulu', 'dalam',
            'dan', 'dapat', 'dari', 'daripada', 'datang', 'dekat', 'demi', 'demikian',
            'demikianlah', 'dengan', 'depan', 'di', 'dia', 'diakhiri', 'diakhirinya',
            'dialah', 'diantara', 'diantaranya', 'diberi', 'diberikan', 'diberikannya',
            'dibuat', 'dibuatnya', 'didapat', 'didatangkan', 'digunakan', 'diibaratkan',
            'diibaratkannya', 'diingat', 'diingatkan', 'diinginkan', 'dijawab',
            'dijelaskan', 'dijelaskannya', 'dikatakan', 'dikatakannya', 'dikehendaki',
            'diketahui', 'diketahuinya', 'dikira', 'dilakukan', 'dilalui', 'dilihat',
            'dimaksud', 'dimaksudkan', 'dimaksudkannya', 'dimaksudnya', 'diminta',
            'dimintai', 'dimisalkan', 'dimulai', 'dimulailah', 'dimulainya', 'dimungkinkan',
            'dini', 'dipastikan', 'diperbuat', 'diperbuatnya', 'dipergunakan',
            'diperkirakan', 'diperlihatkan', 'diperlukan', 'diperlukannya', 'dipersoalkan',
            'dipertanyakan', 'dipunyai', 'diri', 'dirinya', 'disampaikan', 'disebut',
            'disebutkan', 'disebutkannya', 'disini', 'disinilah', 'ditambahkan',
            'ditandaskan', 'ditanya', 'ditanyai', 'ditanyakan', 'ditegaskan', 'ditujukan',
            'ditunjuk', 'ditunjuki', 'ditunjukkan', 'ditunjukkannya', 'ditunjuknya',
            'dituturkan', 'dituturkannya', 'diucapkan', 'diucapkannya', 'diungkapkan',
            'dong', 'dua', 'dulu', 'empat', 'enggak', 'enggaknya', 'entah', 'entahlah',
            'guna', 'gunakan', 'hal', 'hampir', 'hanya', 'hanyalah', 'hari', 'harus',
            'haruslah', 'harusnya', 'hendak', 'hendaklah', 'hendaknya', 'hingga', 'ia',
            'ialah', 'ibarat', 'ibaratkan', 'ibaratnya', 'ibu', 'ikut', 'ingat',
            'ingat-ingat', 'ingin', 'inginkah', 'inginkan', 'ini', 'inikah', 'inilah',
            'itu', 'itukah', 'itulah', 'jadi', 'jadilah', 'jadinya', 'jangan', 'jangankan',
            'janganlah', 'jauh', 'jawab', 'jawaban', 'jawabnya', 'jelas', 'jelaskan',
            'jelaslah', 'jelasnya', 'jika', 'jikalau', 'juga', 'jumlah', 'jumlahnya',
            'justru', 'kala', 'kalau', 'kalaulah', 'kalaupun', 'kalian', 'kami', 'kamilah',
            'kamu', 'kamulah', 'kan', 'kapan', 'kapankah', 'kapanpun', 'karena',
            'karenanya', 'kasus', 'kata', 'katakan', 'katakanlah', 'katanya', 'ke',
            'keadaan', 'kebetulan', 'kecil', 'kedua', 'keduanya', 'keinginan', 'kelamaan',
            'kelihatan', 'kelihatannya', 'kelima', 'keluar', 'kembali', 'kemudian',
            'kemungkinan', 'kemungkinannya', 'kenapa', 'kepada', 'kepadanya', 'kesampaian',
            'keseluruhan', 'keseluruhannya', 'keterlaluan', 'ketika', 'khususnya', 'kini',
            'kinilah', 'kira', 'kira-kira', 'kiranya', 'kita', 'kitalah', 'kok', 'kurang',
            'lagi', 'lagian', 'lah', 'lain', 'lainnya', 'lalu', 'lama', 'lamanya', 'lanjut',
            'lanjutnya', 'lebih', 'lewat', 'lima', 'luar', 'lusa', 'maka', 'makanya',
            'makin', 'malah', 'malahan', 'mampu', 'mampukah', 'mana', 'manakala', 'manalagi',
            'masa', 'masalah', 'masalahnya', 'masih', 'masihkah', 'masing', 'masing-masing',
            'mau', 'maupun', 'melainkan', 'melakukan', 'melalui', 'melihat', 'melihatnya',
            'memang', 'memastikan', 'memberi', 'memberikan', 'membuat', 'memerlukan',
            'memihak', 'meminta', 'memintakan', 'memisalkan', 'memperbuat', 'mempergunakan',
            'memperkirakan', 'memperlihatkan', 'mempersiapkan', 'mempersoalkan',
            'mempertanyakan', 'mempunyai', 'memulai', 'memungkinkan', 'menaiki', 'menambahkan',
            'menandaskan', 'menanti', 'menanti-nanti', 'menantikan', 'menanya', 'menanyai',
            'menanyakan', 'mendapat', 'mendapatkan', 'mendatang', 'mendatangi', 'mendatangkan',
            'menegaskan', 'mengakhiri', 'mengapa', 'mengatakan', 'mengatakannya', 'mengenai',
            'mengerjakan', 'mengetahui', 'menggunakan', 'menghendaki', 'mengibaratkan',
            'mengibaratkannya', 'mengingat', 'mengingatkan', 'menginginkan', 'mengira',
            'mengucapkan', 'mengucapkannya', 'mengungkapkan', 'menjadi', 'menjawab',
            'menjelaskan', 'menuju', 'menunjuk', 'menunjuki', 'menunjukkan', 'menunjuknya',
            'menurut', 'menuturkan', 'menyampaikan', 'menyangkut', 'menyatakan', 'menyebutkan',
            'menyeluruh', 'menyiapkan', 'merasa', 'mereka', 'merekalah', 'merupakan',
            'meski', 'meskipun', 'meyakini', 'meyakinkan', 'minta', 'mirip', 'misal',
            'misalkan', 'misalnya', 'mula', 'mulai', 'mulailah', 'mulanya', 'mungkin',
            'mungkinkah', 'nah', 'naik', 'namun', 'nanti', 'nantinya', 'nyaris', 'nyatanya',
            'oleh', 'olehnya', 'pada', 'padahal', 'padanya', 'pak', 'paling', 'panjang',
            'pantas', 'para', 'pasti', 'pastilah', 'per', 'percuma', 'pergi', 'pernah',
            'perlu', 'perlukah', 'perlunya', 'pertama', 'pertama-tama', 'pertanyaan',
            'pertanyakan', 'pihak', 'pihaknya', 'pukul', 'pula', 'pun', 'punya', 'rasa',
            'rasanya', 'rata', 'rupanya', 'saat', 'saatnya', 'saja', 'sajalah', 'saling',
            'sama', 'sama-sama', 'sambil', 'sampai', 'sampai-sampai', 'sampaikan', 'sana',
            'sangat', 'sangatlah', 'satu', 'saya', 'sayalah', 'se', 'sebab', 'sebabnya',
            'sebagai', 'sebagaimana', 'sebagainya', 'sebagian', 'sebaik', 'sebaik-baiknya',
            'sebaiknya', 'sebaliknya', 'sebanyak', 'sebegini', 'sebegitu', 'sebelum',
            'sebelumnya', 'sebenarnya', 'seberapa', 'sebesar', 'sebetulnya', 'sebisanya',
            'sebuah', 'sebut', 'sebutlah', 'sebutnya', 'secara', 'secukupnya', 'sedang',
            'sedangkan', 'sedemikian', 'sedikit', 'sedikitnya', 'seenaknya', 'segala',
            'segalanya', 'segera', 'seharusnya', 'sehingga', 'seingat', 'sejak', 'sejauh',
            'sejenak', 'sejumlah', 'sekadar', 'sekadarnya', 'sekali', 'sekali-kali',
            'sekalian', 'sekaligus', 'sekalipun', 'sekarang', 'sekarang', 'sekecil',
            'seketika', 'sekiranya', 'sekitar', 'sekitarnya', 'sekurang-kurangnya',
            'sekurangnya', 'sela', 'selain', 'selaku', 'selalu', 'selama', 'selama-lamanya',
            'selamanya', 'selanjutnya', 'seluruh', 'seluruhnya', 'semacam', 'semakin',
            'semampu', 'semampunya', 'semasa', 'semasih', 'semata', 'semata-mata', 'semaunya',
            'sementara', 'semisal', 'semisalnya', 'sempat', 'semua', 'semuanya', 'semula',
            'sendiri', 'sendirian', 'sendirinya', 'seolah', 'seolah-olah', 'seorang',
            'sepanjang', 'sepantasnya', 'sepantasnyalah', 'seperlunya', 'seperti',
            'sepertinya', 'sepihak', 'sering', 'seringnya', 'serta', 'serupa', 'sesaat',
            'sesama', 'sesampai', 'sesegera', 'sesekali', 'seseorang', 'sesuatu', 'sesuatunya',
            'sesudah', 'sesudahnya', 'setelah', 'setelahnya', 'setempat', 'setengah',
            'seterusnya', 'setiap', 'setiba', 'setibanya', 'setidak-tidaknya', 'setidaknya',
            'setinggi', 'seusai', 'sewaktu', 'siap', 'siapa', 'siapakah', 'siapapun',
            'sini', 'sinilah', 'soal', 'soalnya', 'suatu', 'sudah', 'sudahkah', 'sudahlah',
            'supaya', 'tadi', 'tadinya', 'tahu', 'tahun', 'tak', 'tambah', 'tambahnya',
            'tampak', 'tampaknya', 'tandas', 'tandasnya', 'tanpa', 'tanya', 'tanyakan',
            'tanyanya', 'tapi', 'tegas', 'tegasnya', 'telah', 'tempat', 'tengah', 'tentang',
            'tentu', 'tentulah', 'tentunya', 'tepat', 'terakhir', 'terasa', 'terbanyak',
            'terdahulu', 'terdapat', 'terdiri', 'terhadap', 'terhadapnya', 'teringat',
            'teringat-ingat', 'terjadi', 'terjadilah', 'terjadinya', 'terkira', 'terlalu',
            'terlebih', 'terlihat', 'termasuk', 'ternyata', 'tersampaikan', 'tersebut',
            'tersebutlah', 'tertentu', 'tertuju', 'terus', 'terutama', 'tetap', 'tetapi',
            'tiap', 'tiba', 'tiba-tiba', 'tidak', 'tidakkah', 'tidaklah', 'tiga', 'tinggi',
            'toh', 'tunjuk', 'turut', 'tutur', 'tuturnya', 'ucap', 'ucapnya', 'ujar',
            'ujarnya', 'umum', 'umumnya', 'ungkap', 'ungkapnya', 'untuk', 'usai', 'usai',
            'waduh', 'wah', 'wahai', 'waktu', 'waktunya', 'walau', 'walaupun', 'wong',
            'yaitu', 'yakin', 'yakni', 'yang'
        }

        # Tambahan stopwords untuk domain akademik (HANYA kata yang tidak informatif)
        self.academic_stopwords = {
            'doi', 'vol', 'pp', 'et', 'al', 'page', 'pages', 'volume', 'issue',
            'isbn', 'issn', 'http', 'https', 'www', 'com', 'org', 'edu'
        }

        # Gabungkan semua stopwords
        self.stop_words.update(common_stopwords)
        self.stop_words.update(indonesian_stopwords)
        self.stop_words.update(self.academic_stopwords)

        self.tfidf_matrix = None
        self.papers = []
        self.paper_texts = []
    
    def _create_vectorizer(self, n_docs):
        """Create TF-IDF vectorizer dengan parameter yang sesuai jumlah dokumen"""
        # Adjust parameters based on corpus size to avoid pruning errors
        if n_docs <= 1:
            min_df = 1
            max_df = 1.0
        elif n_docs <= 5:
            min_df = 1
            max_df = 1.0
        elif n_docs <= 20:
            min_df = 1
            max_df = 0.95
        else:
            min_df = 1
            max_df = 0.9

        # Gunakan stopwords yang sudah didefinisikan di __init__
        # Konversi ke list karena TfidfVectorizer membutuhkan list
        return TfidfVectorizer(
            max_features=5000,
            stop_words=list(self.stop_words),  # Gunakan stopwords lengkap
            ngram_range=(1, 2),
            min_df=min_df,
            max_df=max_df,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'  # Hanya kata minimal 3 huruf
        )
    
    def preprocess_text(self, text):
        """
        Preprocessing teks:
        1. Lowercase
        2. Remove special characters & numbers
        3. Tokenization
        4. Remove stopwords
        5. Stemming/Lemmatization
        """
        if not text:
            return ""
        
        # 1. Lowercase
        text = str(text).lower()
        
        # 2. Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # 3. Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # 4. Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # 5. Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 6. Tokenization
        try:
            tokens = word_tokenize(text)
        except:
            tokens = text.split()

        # 7. Remove stopwords and short words (minimal 3 karakter)
        tokens = [t for t in tokens if t not in self.stop_words and len(t) >= 3]

        # 8. Lemmatization (lebih baik dari stemming untuk NLP)
        try:
            tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
        except:
            pass  # Skip lemmatization if fails

        # 9. Filter lagi setelah lemmatization untuk memastikan tidak ada stopwords
        tokens = [t for t in tokens if t not in self.stop_words and len(t) >= 3]

        return ' '.join(tokens)
    
    def fit(self, papers):
        """
        Fit TF-IDF vectorizer dengan papers
        
        Args:
            papers: List of paper dictionaries dengan 'title' dan 'abstract'
        """
        self.papers = papers
        self.paper_texts = []
        
        if not papers:
            return self
        
        for paper in papers:
            # Gabungkan title dan abstract
            title = paper.get('title', '') or ''
            abstract = paper.get('abstract', paper.get('snippet', '')) or ''
            combined = f"{title} {title} {abstract}"  # Title diulang untuk bobot lebih
            
            # Preprocess
            processed = self.preprocess_text(combined)
            self.paper_texts.append(processed if processed else title.lower())
        
        # Filter out empty texts
        valid_indices = [i for i, t in enumerate(self.paper_texts) if t.strip()]
        
        if not valid_indices:
            print("[WARNING] No valid texts for TF-IDF after preprocessing")
            return self
        
        # Create vectorizer with appropriate parameters
        self.vectorizer = self._create_vectorizer(len(valid_indices))
        
        # Fit TF-IDF with error handling
        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.paper_texts)
            print(f"[DEBUG] TF-IDF fitted: {self.tfidf_matrix.shape}")
        except ValueError as e:
            print(f"[WARNING] TF-IDF error: {e}")
            # Fallback: use simpler vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words=list(self.stop_words),
                ngram_range=(1, 1),
                min_df=1,
                max_df=1.0,
                token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'  # Hanya kata minimal 3 huruf
            )
            try:
                self.tfidf_matrix = self.vectorizer.fit_transform(self.paper_texts)
                print(f"[DEBUG] TF-IDF fallback fitted: {self.tfidf_matrix.shape}")
            except Exception as e2:
                print(f"[ERROR] TF-IDF fallback also failed: {e2}")
                self.tfidf_matrix = None
        
        return self
    
    def calculate_similarity_to_query(self, query):
        """
        Hitung Cosine Similarity antara query dengan semua papers
        
        Args:
            query: String query dari user
            
        Returns:
            List of (paper_index, similarity_score) sorted by score descending
        """
        if self.tfidf_matrix is None or len(self.papers) == 0:
            return []
        
        # Preprocess query
        processed_query = self.preprocess_text(query)
        
        # Transform query ke TF-IDF vector
        query_vector = self.vectorizer.transform([processed_query])
        
        # Hitung Cosine Similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Create list of (index, score) dan sort
        scored_papers = [(i, score) for i, score in enumerate(similarities)]
        scored_papers.sort(key=lambda x: x[1], reverse=True)
        
        return scored_papers
    
    def get_similar_papers(self, paper_index, top_n=5):
        """
        Dapatkan papers yang mirip dengan paper tertentu
        
        Args:
            paper_index: Index dari paper referensi
            top_n: Jumlah rekomendasi
            
        Returns:
            List of (paper_index, similarity_score)
        """
        if self.tfidf_matrix is None or paper_index >= len(self.papers):
            return []
        
        # Get TF-IDF vector untuk paper referensi
        paper_vector = self.tfidf_matrix[paper_index]
        
        # Hitung similarity dengan semua papers
        similarities = cosine_similarity(paper_vector, self.tfidf_matrix).flatten()
        
        # Sort dan exclude paper itu sendiri
        scored_papers = [(i, score) for i, score in enumerate(similarities) if i != paper_index]
        scored_papers.sort(key=lambda x: x[1], reverse=True)
        
        return scored_papers[:top_n]
    
    def rank_papers_by_relevance(self, query):
        """
        Rank semua papers berdasarkan relevansi dengan query
        
        Args:
            query: Search query
            
        Returns:
            List of papers dengan tambahan field 'relevance_score'
        """
        similarities = self.calculate_similarity_to_query(query)
        
        ranked_papers = []
        for idx, score in similarities:
            paper = self.papers[idx].copy()
            paper['relevance_score'] = round(score * 100, 2)  # Convert ke persentase
            paper['relevance_rank'] = len(ranked_papers) + 1
            ranked_papers.append(paper)
        
        return ranked_papers
    
    def get_recommendations(self, selected_papers, all_papers, top_n=10):
        """
        Content-Based Filtering: Rekomendasikan papers berdasarkan yang dipilih
        
        Args:
            selected_papers: List of papers yang dipilih user
            all_papers: Semua papers untuk direkomendasikan
            top_n: Jumlah rekomendasi
            
        Returns:
            List of recommended papers dengan similarity scores
        """
        if not selected_papers or not all_papers:
            return []
        
        # Gabungkan teks dari selected papers sebagai "user profile"
        selected_texts = []
        for paper in selected_papers:
            title = paper.get('title', '')
            abstract = paper.get('abstract', paper.get('snippet', ''))
            selected_texts.append(f"{title} {abstract}")
        
        user_profile = ' '.join(selected_texts)
        processed_profile = self.preprocess_text(user_profile)
        
        # Prepare all papers untuk comparison
        all_texts = []
        for paper in all_papers:
            title = paper.get('title', '')
            abstract = paper.get('abstract', paper.get('snippet', ''))
            all_texts.append(self.preprocess_text(f"{title} {abstract}"))
        
        # Fit vectorizer dengan semua teks
        combined_texts = all_texts + [processed_profile]
        
        # Use try-catch for vectorizer
        try:
            temp_vectorizer = TfidfVectorizer(
                max_features=3000,
                stop_words=list(self.stop_words),  # Gunakan stopwords lengkap
                ngram_range=(1, 2),
                min_df=1,
                max_df=1.0,  # No max_df limit to avoid pruning
                token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'  # Hanya kata minimal 3 huruf
            )
            tfidf_all = temp_vectorizer.fit_transform(combined_texts)
        except ValueError:
            # Fallback with simpler settings
            temp_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words=list(self.stop_words),
                ngram_range=(1, 1),
                min_df=1,
                max_df=1.0,
                token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'
            )
            tfidf_all = temp_vectorizer.fit_transform(combined_texts)
        
        # User profile vector adalah yang terakhir
        user_vector = tfidf_all[-1]
        paper_vectors = tfidf_all[:-1]
        
        # Hitung similarity
        similarities = cosine_similarity(user_vector, paper_vectors).flatten()
        
        # Create recommendations
        recommendations = []
        selected_titles = {p.get('title', '').lower() for p in selected_papers}
        
        for i, score in enumerate(similarities):
            paper = all_papers[i]
            # Exclude papers yang sudah dipilih
            if paper.get('title', '').lower() not in selected_titles:
                rec = paper.copy()
                rec['similarity_score'] = round(score * 100, 2)
                recommendations.append(rec)
        
        # Sort by similarity dan return top N
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        return recommendations[:top_n]
    
    def get_tfidf_terms(self, paper_index, top_n=10):
        """
        Dapatkan top TF-IDF terms untuk paper tertentu
        
        Args:
            paper_index: Index paper
            top_n: Jumlah terms
            
        Returns:
            List of (term, tfidf_score)
        """
        if self.tfidf_matrix is None or paper_index >= len(self.papers):
            return []
        
        feature_names = self.vectorizer.get_feature_names_out()
        paper_vector = self.tfidf_matrix[paper_index].toarray().flatten()
        
        # Get top terms
        top_indices = paper_vector.argsort()[-top_n:][::-1]
        top_terms = [(feature_names[i], round(paper_vector[i], 4)) for i in top_indices if paper_vector[i] > 0]
        
        return top_terms
    
    def explain_similarity(self, paper1_idx, paper2_idx):
        """
        Jelaskan mengapa dua papers mirip
        
        Returns:
            Dictionary dengan explanation
        """
        if self.tfidf_matrix is None:
            return {}
        
        terms1 = dict(self.get_tfidf_terms(paper1_idx, 20))
        terms2 = dict(self.get_tfidf_terms(paper2_idx, 20))
        
        # Find common terms
        common_terms = set(terms1.keys()) & set(terms2.keys())
        
        # Calculate contribution
        contributions = []
        for term in common_terms:
            score = terms1[term] * terms2[term]
            contributions.append((term, score))
        
        contributions.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'common_terms': list(common_terms),
            'top_contributing_terms': contributions[:5],
            'paper1_unique_terms': list(set(terms1.keys()) - common_terms)[:5],
            'paper2_unique_terms': list(set(terms2.keys()) - common_terms)[:5]
        }


# Fungsi helper untuk integrasi dengan app.py
def rank_papers_with_cbf(papers, query):
    """
    Rank papers dengan Content-Based Filtering
    
    Args:
        papers: List of papers dari scraping
        query: User's search query
        
    Returns:
        Papers yang sudah di-rank dengan relevance score
    """
    if not papers:
        return papers
    
    cbf = ContentBasedFilter()
    cbf.fit(papers)
    ranked = cbf.rank_papers_by_relevance(query)
    
    return ranked


def get_paper_recommendations(selected_papers, all_papers, top_n=10):
    """
    Dapatkan rekomendasi paper berdasarkan yang dipilih user
    
    Args:
        selected_papers: Papers yang dipilih user
        all_papers: Semua papers available
        top_n: Jumlah rekomendasi
        
    Returns:
        List of recommended papers dengan similarity scores
    """
    cbf = ContentBasedFilter()
    return cbf.get_recommendations(selected_papers, all_papers, top_n)


def find_similar_papers(reference_paper, all_papers, top_n=5):
    """
    Cari papers yang mirip dengan paper referensi
    
    Args:
        reference_paper: Paper yang jadi referensi
        all_papers: Semua papers untuk dicari
        top_n: Jumlah hasil
        
    Returns:
        List of similar papers dengan scores
    """
    cbf = ContentBasedFilter()
    
    # Add reference paper to list for comparison
    papers_with_ref = [reference_paper] + all_papers
    cbf.fit(papers_with_ref)
    
    similar = cbf.get_similar_papers(0, top_n)
    
    results = []
    for idx, score in similar:
        if idx > 0:  # Skip reference paper itself
            paper = all_papers[idx - 1].copy()
            paper['similarity_score'] = round(score * 100, 2)
            results.append(paper)
    
    return results


def get_cbf_calculation_details(selected_papers, query):
    """
    Dapatkan detail perhitungan CBF untuk papers yang dipilih
    Menampilkan proses TF-IDF dan Cosine Similarity
    
    Args:
        selected_papers: Papers yang dipilih user
        query: Search query
        
    Returns:
        Dictionary dengan detail perhitungan
    """
    if not selected_papers:
        return {'error': 'No papers selected'}
    
    cbf = ContentBasedFilter()
    cbf.fit(selected_papers)
    
    # Preprocessing details
    preprocessing_results = []
    for i, paper in enumerate(selected_papers[:5]):
        original_text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        preprocessed = cbf.paper_texts[i] if i < len(cbf.paper_texts) else ''
        preprocessing_results.append({
            'title': paper.get('title', '')[:60],
            'original': original_text[:300],
            'preprocessed': preprocessed[:300]
        })
    
    # TF-IDF details
    tfidf_data = {
        'total_terms': 0,
        'total_docs': len(selected_papers),
        'top_terms': [],
        'matrix': []
    }
    
    if cbf.vectorizer and cbf.tfidf_matrix is not None:
        feature_names = cbf.vectorizer.get_feature_names_out()
        tfidf_data['total_terms'] = len(feature_names)
        
        # Get top terms by average TF-IDF score
        avg_scores = np.mean(cbf.tfidf_matrix.toarray(), axis=0)
        top_indices = np.argsort(avg_scores)[::-1][:30]
        
        for idx in top_indices:
            tfidf_data['top_terms'].append({
                'term': feature_names[idx],
                'score': float(avg_scores[idx]),
                'df': int(np.sum(cbf.tfidf_matrix.toarray()[:, idx] > 0))
            })
    
    # Calculate similarity to query
    papers_with_similarity = []
    if cbf.tfidf_matrix is not None:
        query_preprocessed = cbf.preprocess_text(query)
        try:
            query_vector = cbf.vectorizer.transform([query_preprocessed])
            similarities = cosine_similarity(query_vector, cbf.tfidf_matrix)[0]
            
            for i, paper in enumerate(selected_papers):
                sim = similarities[i] if i < len(similarities) else 0
                papers_with_similarity.append({
                    'title': paper.get('title', ''),
                    'authors': paper.get('authors', 'Unknown'),
                    'year': paper.get('year', ''),
                    'citations': paper.get('citations', 0),
                    'similarity': float(sim),
                    'relevance_score': paper.get('relevance_score', 0)
                })
        except:
            papers_with_similarity = [{
                'title': p.get('title', ''),
                'authors': p.get('authors', 'Unknown'),
                'year': p.get('year', ''),
                'citations': p.get('citations', 0),
                'similarity': p.get('relevance_score', 0) / 100,
                'relevance_score': p.get('relevance_score', 0)
            } for p in selected_papers]
    
    # Sort by similarity for ranking
    ranking = sorted(papers_with_similarity, key=lambda x: x['similarity'], reverse=True)
    
    # Similarity matrix between papers
    similarity_matrix = []
    if cbf.tfidf_matrix is not None and len(selected_papers) > 1:
        sim_matrix = cosine_similarity(cbf.tfidf_matrix)
        for i in range(min(len(selected_papers), 10)):
            row = []
            for j in range(min(len(selected_papers), 10)):
                row.append(float(sim_matrix[i][j]))
            similarity_matrix.append(row)
    
    # Hasil perhitungan lengkap
    calculation_details = {
        'query': query,
        'total_papers': len(selected_papers),
        'preprocessing': preprocessing_results,
        'tfidf': tfidf_data,
        'papers': papers_with_similarity,
        'ranking': ranking,
        'similarity_matrix': similarity_matrix,
        'papers_analysis': [],
        'preprocessing_info': {
            'steps': [
                '1. Case Folding (lowercase)',
                '2. Tokenisasi',
                '3. Penghapusan Stopwords',
                '4. Lemmatisasi'
            ]
        },
        'tfidf_info': {
            'formula': 'TF-IDF = TF(t,d) × IDF(t)',
            'tf_formula': 'TF(t,d) = frekuensi term t dalam dokumen d',
            'idf_formula': 'IDF(t) = log(N / df(t)) + 1',
            'description': 'TF-IDF memberikan bobot tinggi pada kata yang sering muncul di dokumen tertentu tapi jarang di dokumen lain'
        },
        'cosine_info': {
            'formula': 'Cosine Similarity = (A · B) / (||A|| × ||B||)',
            'description': 'Mengukur kemiripan berdasarkan sudut antara dua vektor dokumen (0-1)'
        }
    }
    
    # Analisis setiap paper (legacy support)
    for i, paper in enumerate(selected_papers):
        paper_analysis = {
            'index': i + 1,
            'title': paper.get('title', '')[:80],
            'relevance_score': paper.get('relevance_score', 0),
            'top_tfidf_terms': [],
            'preprocessed_sample': ''
        }
        
        # Get top TF-IDF terms
        if cbf.tfidf_matrix is not None and i < len(cbf.papers):
            terms = cbf.get_tfidf_terms(i, 8)
            paper_analysis['top_tfidf_terms'] = [
                {'term': t, 'weight': round(w, 4)} for t, w in terms
            ]
        
        # Get preprocessed text sample
        if i < len(cbf.paper_texts):
            text = cbf.paper_texts[i]
            paper_analysis['preprocessed_sample'] = text[:150] + '...' if len(text) > 150 else text
        
        calculation_details['papers_analysis'].append(paper_analysis)
    
    # Statistik keseluruhan
    scores = [p.get('relevance_score', 0) for p in selected_papers]
    calculation_details['statistics'] = {
        'average_relevance': round(sum(scores) / len(scores), 2) if scores else 0,
        'max_relevance': round(max(scores), 2) if scores else 0,
        'min_relevance': round(min(scores), 2) if scores else 0,
        'total_unique_terms': len(cbf.vectorizer.get_feature_names_out()) if cbf.vectorizer else 0
    }
    
    return calculation_details


# Test
if __name__ == "__main__":
    print("Testing Content-Based Filtering...")
    
    # Sample papers
    papers = [
        {
            'title': 'Deep Learning for Natural Language Processing',
            'abstract': 'This paper presents a comprehensive survey of deep learning techniques applied to NLP tasks including sentiment analysis, machine translation, and text classification.'
        },
        {
            'title': 'Machine Learning in Healthcare',
            'abstract': 'We explore applications of machine learning algorithms in medical diagnosis, patient outcome prediction, and drug discovery.'
        },
        {
            'title': 'Neural Networks for Image Recognition',
            'abstract': 'This study investigates convolutional neural networks for image classification and object detection tasks.'
        },
        {
            'title': 'Text Mining and Sentiment Analysis',
            'abstract': 'A study on extracting opinions and sentiments from text data using NLP and machine learning techniques.'
        },
        {
            'title': 'Reinforcement Learning in Robotics',
            'abstract': 'Application of reinforcement learning algorithms for robot navigation and manipulation tasks.'
        }
    ]
    
    cbf = ContentBasedFilter()
    cbf.fit(papers)
    
    # Test 1: Query similarity
    print("\n1. Query: 'natural language processing text analysis'")
    results = cbf.calculate_similarity_to_query('natural language processing text analysis')
    for idx, score in results[:3]:
        print(f"   {papers[idx]['title'][:50]}... Score: {score:.4f}")
    
    # Test 2: Similar papers
    print("\n2. Papers similar to 'Deep Learning for NLP':")
    similar = cbf.get_similar_papers(0, 3)
    for idx, score in similar:
        print(f"   {papers[idx]['title'][:50]}... Score: {score:.4f}")
    
    # Test 3: TF-IDF terms
    print("\n3. Top TF-IDF terms for 'Deep Learning for NLP':")
    terms = cbf.get_tfidf_terms(0, 5)
    for term, score in terms:
        print(f"   {term}: {score}")
    
    print("\nContent-Based Filtering module ready!")
