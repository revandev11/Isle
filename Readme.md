# Recruiter LinkedIn Axtarışı

Azərbaycandakı şirkətlərdə işləyən **IT recruiter** və **talent acquisition** mütəxəssislərinin LinkedIn profil linklərini tapır və CSV faylına yazır.

Skript [SerpAPI](https://serpapi.com) vasitəsilə Google nəticələrini oxuyur. LinkedIn-in özünə daxil olmur və scrape etmir, yalnız Google-un indeksləyib göstərdiyi açıq nəticələrdən istifadə edir.

## Tələblər

- Python 3.8 və ya daha yeni
- `requests` kitabxanası
- SerpAPI hesabı və API key

## Quraşdırma

1. Kitabxananı quraşdır:

   ```
   pip install requests
   ```

   `pip` tanınmasa: `python -m pip install requests`

2. [serpapi.com](https://serpapi.com) saytında qeydiyyatdan keç və dashboard-dan API key-i kopyala.

3. Key-i skripta ötür
   Skriptdə bu sətir olduğu kimi qalmalıdır:

   ```python
   API_KEY = os.getenv("SERPAPI_KEY")
   ```

   Terminalda (Windows PowerShell):

   ```
   $env:SERPAPI_KEY="sənin_keyin"
   ```

## İstifadə

Terminalda faylın olduğu qovluğa keç və işlət:

```
cd C:\yol\qovluq
python recruiter_linkedin_serpapi.py
```

Fayl adında boşluq olmamalıdır. Boşluq varsa dırnaq işlət: `python "fayl adı.py"`.

## Nəticə

Skript ekranda hər tapılan profilin adını və linkini çap edir, sonda isə qovluqda `recruiters_linkedin_TARİX.csv` faylı yaranır. Excel-də aça bilərsən.

| Sütun | Məna |
|-------|------|
| Ad | Profildəki ad |
| Başlıq | Vəzifə və şirkət |
| LinkedIn | Profilin linki |
| Axtarış | Hansı sorğudan çıxdığı (ümumi və ya şirkət adı) |
| Status | Özün doldurmaq üçün (məs. "yazıldı", "cavab gəldi") |
| Qeyd | Özün doldurmaq üçün |

## Ayarlar

Skriptin yuxarısındakı dəyişənləri redaktə edə bilərsən:

- `TITLES`: axtarılan vəzifələr
- `COMPANIES`: axtarılan şirkətlər
- `PAGES_PER_QUERY`: hər sorğu üçün neçə səhifə nəticə (hər səhifə ~10 nəticə)

## Kredit limiti

SerpAPI-də hər sorğu planındakı 1 axtarış krediti sərf edir. Skript default olaraq 16 sorğu göndərir (1 ümumi və hər şirkət üçün 1). Pulsuz planın limiti kiçikdir, ona görə əvvəlcə `COMPANIES` siyahısını 3-4 şirkətə qısaltmaq məsləhətdir. Cari limiti SerpAPI qiymət səhifəsindən yoxla.

## Məhdudiyyətlər

- Google bütün LinkedIn profillərini indeksləmir, ona görə bəzi recruiter-lər nəticədə çıxmaya bilər.
- Başlıqdakı şirkət köhnə ola bilər. Yazmazdan əvvəl profili açıb yoxla.
- LinkedIn-də tanımadığın insanlara gündə çox sorğu göndərmə, hesab məhdudlaşdırıla bilər.
