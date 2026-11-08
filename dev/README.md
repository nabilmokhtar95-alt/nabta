# تطوير جنينة نبتة

- `src/nabta-garden.html` : مصدر اللعبة (ده اللي بيتعدّل)
- `make.py` : بيبني `../game.html` (المنشور) و`out/test28.html` (نسخة الاختبار) و`out/nabta-game.html` (نسخة claude.ai)
  - في `game.html` المنشورة الصور بتطلع لملفات في `../ga/` (أسماءها من محتواها)، عشان الصفحة تبقى ٧٠٠ كيلو بدل ٧.٥ ميجا. `ga/index.js` فيه قايمتهم والـ service worker بيخزّنهم للعب من غير نت. متعدّلش `ga/` بإيدك.
- `thumbs.py` : بيعمل صور صغيرة للكروت في `../toys/s/` من صور `../toys/`. شغّله بعد إضافة صورة لعبة جديدة (لو نسيته المتجر بيرجع للصورة الكبيرة لوحده).
- `tests/` : اختبارات Playwright للعبة. بتتشغّل من جوه `out/` بعد `python3 make.py` و`cp ../phaser.min.js out/`
- `tests/site.js` : اختبار للموقع كله (الطلب، الحكايات، بوابة الكبار، الصور). شغّل `npx http-server -p 8765 -s -c-1 .` من جذر المشروع، وبعدين `NODE_PATH=$(npm root -g) node dev/tests/site.js`
- `voice/split3.py` : بيقسّم ملفات البلوكات اللي في `voice/raw` لجمل ويحدّث `voice/index.json`

الحكايات: الفيديوهات في `../videos/` (mp4 + webm + صورة webp)، وقايمتها في `STORIES` جوه المصدر.
واتساب الطلبات: اكتب الرقم في `const WA=''` في `index.html` ويظهر زرار «ابعتوها واتساب» بالرسالة جاهزة.

بعد أي تعديل: `python3 dev/make.py`، وزوّد رقم النسخة `V` في `sw.js`.
