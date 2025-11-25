import re
from bs4 import BeautifulSoup
import google.generativeai as genai
import google.generativeai as genai
import json
import logging
import requests

class GeminiCopywriter:
    def __init__(self, html_content, api_key, style='pink_curhat', rewrite_copywriting=False, custom_prompt='', design_tokens=None):
        self.html_content = html_content
        self.api_key = api_key
        self.style = style
        self.rewrite_copywriting = rewrite_copywriting
        self.custom_prompt = custom_prompt
        self.design_tokens = design_tokens

    def generate(self):
        import time
        
        logging.info(f"  → Configuring Gemini with API key...")
        genai.configure(api_key=self.api_key)
        
        # Define models to try in order
        models_to_try = ['gemini-2.0-flash-lite', 'gemini-1.5-flash']
        
        # Define Style Guides
        style_guides = {
            'pink_curhat': """
🎨 STYLE: PINK CURHAT (Feminine & Friendly)
- Colors: Primary Pink (#db2777), Background Soft Pink (#fdf2f8), White Cards
- Fonts: 'Playfair Display' (Headings), 'Inter' (Body)
- Shapes: Rounded corners (rounded-3xl), soft shadows, floating cards
- Vibe: Friendly, personal, "bestie" tone, warm, trustworthy
- Decor: Heart icons, soft gradients, dashed borders
""",
            'minimalist_clean': """
🎨 STYLE: MINIMALIST CLEAN (Professional & Modern)
- Colors: Slate/Gray (#0f172a), White Background, Subtle Borders
- Fonts: 'Inter' or 'Plus Jakarta Sans' (Clean Sans-serif)
- Shapes: Sharp or slightly rounded (rounded-lg), clean lines, ample whitespace
- Vibe: Professional, corporate, trustworthy, serious but modern
- Decor: Minimal icons, thin borders, subtle shadows
""",
            'bold_dark': """
🎨 STYLE: BOLD DARK (High Impact & Masculine)
- Colors: Dark Background (#111), White Text, Gold/Amber Accents (#fbbf24)
- Fonts: 'Oswald' (Headings), 'Roboto' (Body)
- Shapes: Sharp edges, high contrast, bold borders
- Vibe: Aggressive, confident, premium, exclusive
- Decor: Strong shadows, metallic gradients, bold dividers
""",
            'luxury_elegant': """
🎨 STYLE: LUXURY ELEGANT (Premium & Exclusive)
- Colors: Black/Deep Navy (#0f172a), Gold/Bronze Accents (#d4af37), White Text
- Fonts: 'Playfair Display' or 'Cinzel' (Headings), 'Lato' (Body)
- Shapes: Sharp corners, thin elegant lines, ample whitespace
- Vibe: Expensive, sophisticated, high-end, exclusive
- Decor: Gold borders, marble textures, minimalist icons
""",
            'eco_natural': """
🎨 STYLE: ECO NATURAL (Organic & Fresh)
- Colors: Sage Green (#578a62), Earthy Brown (#8d6e63), Cream Background (#fbf7f5)
- Fonts: 'Nunito' or 'Quicksand' (Rounded Sans), 'Merriweather' (Serif)
- Shapes: Soft organic shapes, leaf motifs, rounded corners
- Vibe: Natural, healthy, sustainable, calming
- Decor: Plant icons, paper textures, soft shadows
""",
            'tech_modern': """
🎨 STYLE: TECH MODERN (SaaS & Futuristic)
- Colors: Electric Blue (#3b82f6), Deep Purple (#6366f1), Dark Mode Background
- Fonts: 'Inter' or 'Space Grotesk' (Modern Sans)
- Shapes: Glassmorphism (blur effects), gradients, rounded-xl
- Vibe: Innovative, digital, trustworthy, fast
- Decor: Grid patterns, glowing effects, gradient text
""",
            'high_energy': """
🎨 STYLE: HIGH ENERGY (Urgent & Salesy)
- Colors: Bright Red (#ef4444), Vibrant Orange (#f97316), White Background
- Fonts: 'Montserrat' (Bold Headings), 'Open Sans' (Body)
- Shapes: Slanted dividers, bold buttons, arrows
- Vibe: Urgent, exciting, action-oriented, viral
- Decor: Lightning icons, bold borders, drop shadows
""",
            'ebook_bestseller': """
🎨 STYLE: EBOOK BEST SELLER (Professional & Authoritative)
- Colors: Navy Blue (#1e3a8a), Clean White, Gold/Yellow Accents (#facc15)
- Fonts: 'Merriweather' (Serif for authority), 'Inter' (Sans for readability)
- Shapes: 3D Book Cover effects (shadow-xl), clean cards, checkmark lists
- Vibe: Knowledgeable, trustworthy, premium, educational
- Decor: Book icons, author profile styling, testimonial quotes
"""
        }
        
        # Use design tokens if available (from reference URL)
        if self.design_tokens:
            selected_style = f"""
🎨 STYLE: COPIED FROM REFERENCE URL ({self.design_tokens.get('vibe', 'Custom Style')})
- Colors: {self.design_tokens.get('colors')}
- Fonts: {self.design_tokens.get('fonts')}
- Shapes: {self.design_tokens.get('shapes')}
- Components: {self.design_tokens.get('components')}
- Vibe: {self.design_tokens.get('vibe')}
"""
        elif self.style == 'reference_style':
            # If reference_style is selected but no design_tokens, use a neutral prompt
            selected_style = """
🎨 STYLE: REFERENCE LINK (Awaiting URL)
- Please provide a reference URL to extract design tokens.
- Using minimal default styling for now.
"""
        elif self.style == 'custom' and self.custom_prompt:
            selected_style = f"""
🎨 STYLE: CUSTOM (User-Defined)
{self.custom_prompt}
"""
        else:
            selected_style = style_guides.get(self.style, style_guides['pink_curhat'])

        # Define Copywriting Instructions
        if self.rewrite_copywriting:
            copy_instruction = """
✍️ COPYWRITING INSTRUCTIONS (REWRITE MODE):
1. TULIS ULANG semua teks agar lebih MENJUAL, PERSUASIF, dan ENAK DIBACA.
2. Gunakan bahasa yang sesuai dengan Style Vibe (misal: Pink Curhat = pakai "Bestie", "Kamu", dll).
3. Buat headline lebih nendang & catchy.
4. TAPI: JANGAN ubah makna inti atau fakta produk (harga, fitur utama tetap sama).
"""
        else:
            copy_instruction = """
🔒 CONTENT PRESERVATION INSTRUCTIONS (STRICT):
1. JANGAN UBAH TEKS APAPUN. Gunakan teks persis seperti di HTML Input.
2. JANGAN ringkas/summarize paragraf.
3. JANGAN hilangkan item list.
4. Copy-paste semua teks dari input ke desain baru.
"""

        # Construct the Master Prompt
        prompt = f"""
Role: You are a World-Class Frontend Developer & UI/UX Designer.
Task: Redesign the provided HTML Input to match the target "{self.style}" style.

{selected_style}

{copy_instruction}

⚠️ CRITICAL REQUIREMENTS (DO NOT IGNORE):
1. **FULL CONTENT PRESERVATION**: 
   - You MUST include ALL sections from the input HTML.
   - You MUST include ALL images (use exact URLs from input).
   - You MUST include ALL feature cards, testimonials, and list items.
   - If the input has a grid of 4 items, your output MUST have a grid of 4 items.
   - If the input has a countdown timer script, you MUST preserve it and make it work.

2. **TECHNICAL EXECUTION**:
   - Use Tailwind CSS (via CDN) for styling.
   - Use Google Fonts (link in head).
   - Write valid, responsive HTML5.
   - Ensure mobile responsiveness (mobile-first approach).
   - Add custom CSS in <style> tags for specific effects (gradients, animations) that Tailwind can't handle perfectly.

3. **OUTPUT FORMAT**:
   - Return ONLY the raw HTML code (starting with <!DOCTYPE html>).
   - Do not wrap in markdown code blocks (no ```html).
   - Do not add explanations.

=== HTML INPUT START ===
{self.html_content}
=== HTML INPUT END ===

ACTION: Redesign this HTML now. Make it look expensive and professional.
"""

        # Retry Loop with Model Fallback
        for model_name in models_to_try:
            logging.info(f"  → Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            for attempt in range(3): # 3 attempts per model
                try:
                    logging.info(f"    → Attempt {attempt+1}/3...")
                    response = model.generate_content(prompt)
                    html_body = response.text.strip()
                    
                    # Clean up markdown
                    if html_body.startswith('```'):
                        html_body = re.sub(r'^```html?\n?', '', html_body)
                        html_body = re.sub(r'\n?```$', '', html_body)
                    
                    logging.info(f"  ✓ Generation successful with {model_name}!")
                    return html_body
                    
                except Exception as e:
                    logging.warning(f"    ✗ Attempt {attempt+1} failed: {e}")
                    if "429" in str(e):
                        wait_time = (attempt + 1) * 5 # 5s, 10s, 15s
                        logging.info(f"      → Rate limit hit. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        break # If not rate limit, maybe try next model immediately
        
        # If all models and attempts fail
        logging.error("  ✗ ALL GENERATION ATTEMPTS FAILED.")
        error_msg = """
        <div style="background: #fee2e2; color: #991b1b; padding: 20px; border-radius: 10px; margin: 20px; font-family: sans-serif; text-align: center;">
            <h2 style="margin-top:0">⚠️ Generation Failed</h2>
            <p>Maaf, server AI sedang sibuk (Rate Limit 429). Silakan coba lagi dalam 1 menit.</p>
            <p>Menampilkan HTML asli Anda di bawah ini:</p>
        </div>
        """
        return error_msg + self.html_content

class DesignExtractor:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def extract(self):
        try:
            logging.info(f"Fetching reference URL: {self.url}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Basic cleanup to reduce token count
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style", "svg", "path"]):
                script.decompose()
            
            # Get text structure (first 15000 chars to avoid token limits)
            html_structure = str(soup)[:15000] 
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Analyze this HTML from a website and extract its "Design DNA" into a JSON format.
            I need the visual style tokens so I can replicate the "vibe" on another site.
            
            Extract:
            1. colors: Primary, Secondary, Background, Text colors (hex codes).
            2. fonts: Font families used (guess if not explicit).
            3. shapes: Border radius (rounded, sharp, pill), shadow styles.
            4. vibe: A short description of the visual vibe (e.g., "Minimalist dark mode", "Playful and colorful").
            5. components: How buttons and cards look.

            HTML Snippet:
            {html_structure}

            Return ONLY valid JSON.
            """
            
            response = model.generate_content(prompt)
            text = response.text.replace('```json', '').replace('```', '')
            return json.loads(text)
            
        except Exception as e:
            logging.error(f"Design extraction failed: {e}")
            return None

class GeminiExtractor:
    def __init__(self, html_content, api_key):
        self.html_content = html_content
        self.api_key = api_key
        self.data = {}
        
    def extract(self):
        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""Analyze this HTML code and extract the following information in JSON format:
1. headline: The main headline or title (most prominent)
2. image: URL of the main product/hero image
3. story: The main selling point, problem statement, or story (1-2 sentences)
4. priceOriginal: Original price (if found, format: Rp XXX.XXX)
5. priceDiscount: Discounted price (if found, format: Rp XXX.XXX)
6. benefits: Array of key benefits/features (max 5 items)
7. cta: Call-to-action button text

HTML:
{self.html_content}

Return ONLY valid JSON, no markdown formatting or explanation."""

            response = model.generate_content(prompt)
            result = json.loads(response.text)
            
            self.data = {
                'headline': result.get('headline', ''),
                'image': result.get('image', ''),
                'story': result.get('story', ''),
                'priceOriginal': result.get('priceOriginal', ''),
                'priceDiscount': result.get('priceDiscount', ''),
                'benefits': result.get('benefits', []),
                'cta': result.get('cta', 'Beli Sekarang')
            }
            
            return self.data
            
        except Exception as e:
            print(f"Gemini extraction failed: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback to BeautifulSoup
            try:
                print("Falling back to ContentExtractor...")
                fallback = ContentExtractor(self.html_content)
                data = fallback.extract()
                
                # Render using ThemeRenderer
                renderer = ThemeRenderer()
                # Use 'premium' as default theme since we removed theme selection
                return renderer.render(data, 'premium')
            except Exception as fallback_error:
                print(f"Fallback failed: {fallback_error}")
                traceback.print_exc()
                # Return a basic error HTML if everything fails
                return f"<div class='p-4 text-red-500'>Generation failed. Please check your input HTML. Error: {str(e)}</div>"


class ContentExtractor:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.data = {}

    def extract(self):
        self.data['headline'] = self._get_headline()
        self.data['image'] = self._get_image()
        self.data['story'] = self._get_story()
        self.data['priceOriginal'], self.data['priceDiscount'] = self._get_prices()
        self.data['benefits'] = self._get_benefits()
        self.data['cta'] = self._get_cta()
        return self.data

    def _get_headline(self):
        h1 = self.soup.find('h1')
        if h1: return h1.get_text(strip=True)
        title = self.soup.find('title')
        if title: return title.get_text(strip=True)
        h2 = self.soup.find('h2')
        if h2: return h2.get_text(strip=True)
        return "Judul Tidak Ditemukan"

    def _get_image(self):
        img = self.soup.find('img')
        return img['src'] if img and 'src' in img.attrs else ""

    def _get_story(self):
        paragraphs = self.soup.find_all('p')
        if not paragraphs: return ""
        # Return the longest paragraph as the 'story'
        longest_p = max(paragraphs, key=lambda p: len(p.get_text(strip=True)))
        return longest_p.get_text(strip=True)

    def _get_prices(self):
        text = self.soup.get_text()
        # Regex to find prices like Rp 100.000 or Rp100,000
        matches = re.findall(r'Rp\s?[\d,.]+', text)
        if not matches:
            return "", ""
        if len(matches) == 1:
            return "", matches[0] # Assume only discount price if one found
        # Heuristic: Largest is original, smallest is discount (or just first two)
        # Let's just take first two found for simplicity, assuming order
        return matches[1], matches[0] if len(matches) > 1 else (matches[0], "")

    def _get_benefits(self):
        lis = self.soup.select('ul li')
        if not lis: return []
        return [li.get_text(strip=True) for li in lis]

    def _get_cta(self):
        keywords = ['beli', 'pesan', 'order', 'sekarang', 'diskon', 'promo']
        buttons = self.soup.find_all(['button', 'a'])
        
        for btn in buttons:
            text = btn.get_text(strip=True).lower()
            if any(kw in text for kw in keywords):
                return btn.get_text(strip=True)
        
        return buttons[0].get_text(strip=True) if buttons else "Beli Sekarang"

class ThemeRenderer:
    def __init__(self):
        self.themes = {
            'premium': {
                'container': 'bg-white text-gray-800 font-serif',
                'headline': 'text-3xl font-bold text-slate-900 mb-4 leading-tight',
                'image': 'rounded-2xl shadow-lg mb-6 w-full object-cover',
                'storyBox': 'bg-slate-50 p-6 rounded-xl shadow-sm border border-slate-100 mb-6 text-lg leading-relaxed text-slate-700',
                'priceBox': 'text-center mb-8 p-4 border-y border-slate-200',
                'priceOriginal': 'text-slate-400 line-through text-lg mr-2',
                'priceDiscount': 'text-blue-900 text-4xl font-bold',
                'benefitList': 'space-y-3 mb-8',
                'benefitItem': 'flex items-start text-slate-700 text-lg',
                'benefitIcon': 'text-blue-600 mr-3 mt-1',
                'ctaButton': 'block w-full bg-blue-900 text-white text-center py-4 rounded-xl text-xl font-bold shadow-lg hover:bg-blue-800 transition transform hover:-translate-y-1',
                'footer': 'text-center text-slate-400 text-sm mt-8 pb-4',
                'icon': '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>'
            },
            'pedas': {
                'container': 'bg-red-50 text-gray-900 font-sans',
                'headline': 'text-4xl font-black text-red-700 mb-4 uppercase tracking-tighter',
                'image': 'border-4 border-red-600 mb-6 w-full object-cover shadow-[8px_8px_0px_0px_rgba(220,38,38,1)]',
                'storyBox': 'bg-white p-5 border-2 border-red-600 mb-6 text-lg font-medium text-gray-900 shadow-[4px_4px_0px_0px_rgba(220,38,38,0.3)]',
                'priceBox': 'text-center mb-8 bg-yellow-300 p-4 border-2 border-black transform -rotate-1',
                'priceOriginal': 'text-red-800 line-through text-xl font-bold block',
                'priceDiscount': 'text-red-700 text-5xl font-black',
                'benefitList': 'space-y-2 mb-8 border-l-4 border-red-600 pl-4',
                'benefitItem': 'flex items-center text-gray-900 font-bold text-lg',
                'benefitIcon': 'text-red-600 mr-2 text-2xl',
                'ctaButton': 'block w-full bg-red-600 text-white text-center py-4 text-2xl font-black uppercase border-b-8 border-red-800 active:border-b-0 active:mt-2 shadow-xl hover:bg-red-500',
                'footer': 'text-center text-red-400 text-xs mt-8 font-bold uppercase tracking-widest',
                'icon': '💥'
            },
            'sahabat': {
                'container': 'bg-pink-50 text-gray-700 font-sans',
                'headline': 'text-3xl font-bold text-pink-600 mb-4 text-center',
                'image': 'rounded-[30px] mb-6 w-full object-cover border-4 border-white shadow-pink-200 shadow-xl',
                'storyBox': 'bg-white p-6 rounded-[20px] rounded-tl-none shadow-sm mb-6 text-gray-600 leading-relaxed border border-pink-100 relative ml-4',
                'priceBox': 'text-center mb-8 bg-purple-100 rounded-3xl p-6 mx-4',
                'priceOriginal': 'text-purple-400 line-through text-lg block mb-1',
                'priceDiscount': 'text-purple-600 text-4xl font-bold',
                'benefitList': 'space-y-3 mb-8 bg-white p-6 rounded-2xl shadow-sm mx-2',
                'benefitItem': 'flex items-center text-gray-600',
                'benefitIcon': 'text-pink-400 mr-3 bg-pink-100 rounded-full p-1',
                'ctaButton': 'block w-full bg-gradient-to-r from-pink-400 to-purple-500 text-white text-center py-4 rounded-full text-lg font-bold shadow-lg shadow-pink-200 hover:shadow-xl transition hover:scale-105',
                'footer': 'text-center text-pink-300 text-sm mt-8',
                'icon': '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>'
            }
        }

    def render(self, data, theme_name='premium'):
        theme = self.themes.get(theme_name, self.themes['premium'])
        
        benefits_html = ""
        if data.get('benefits'):
            items = "".join([f"""
                <li class="{theme['benefitItem']}">
                    <span class="{theme['benefitIcon']}">{theme['icon']}</span>
                    {item}
                </li>""" for item in data['benefits']])
            benefits_html = f'<ul class="{theme["benefitList"]}">{items}</ul>'

        image_html = ""
        if data.get('image'):
            image_html = f'<img src="{data["image"]}" class="{theme["image"]}" alt="Product Image">'

        # Fix for f-string backslash issue
        story_text = data.get('story', '').replace('\n', '<br>')

        price_html = ""
        if data.get('priceDiscount'):
            price_html = f"""
            <div class="{theme['priceBox']}">
                <span class="{theme['priceOriginal']}">{data.get('priceOriginal', '')}</span>
                <span class="{theme['priceDiscount']}">{data['priceDiscount']}</span>
            </div>"""

        html = f"""
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Playfair+Display:wght@400;700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {{ padding: 0 2px 40px 2px; }}
                .theme-premium {{ font-family: 'Playfair Display', serif; }}
                .theme-pedas {{ font-family: 'Inter', sans-serif; }}
                .theme-sahabat {{ font-family: 'Poppins', sans-serif; }}
                /* Hide scrollbar for clean preview */
                ::-webkit-scrollbar {{ display: none; }}
            </style>
        </head>
        <body class="{theme['container']}">
            <div class="pt-8 pb-12">
                <h1 class="{theme['headline']}">{data.get('headline', '')}</h1>
                
                {image_html}
                
                <div class="{theme['storyBox']}">
                    {story_text}
                </div>

                {price_html}

                {benefits_html}

                <a href="#" class="{theme['ctaButton']}">
                    {data.get('cta', 'Beli Sekarang')}
                </a>

                <div class="{theme['footer']}">
                    &copy; 2024 Brand Name
                </div>
            </div>
        </body>
        </html>
        """
        return html
