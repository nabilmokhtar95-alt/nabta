# تطوير جنينة نبتة

- `src/nabta-garden.html` : مصدر اللعبة (ده اللي بيتعدّل)
- `make.py` : بيبني `../game.html` (المنشور) و`out/test28.html` (نسخة الاختبار) و`out/nabta-game.html` (نسخة claude.ai)
- `tests/` : اختبارات Playwright. بتتشغّل من جوه `out/` بعد `python3 make.py` و`cp ../phaser.min.js out/`
- `voice/split3.py` : بيقسّم ملفات البلوكات اللي في `voice/raw` لجمل ويحدّث `voice/index.json`

بعد أي تعديل: `python3 dev/make.py`، وزوّد رقم النسخة `V` في `sw.js`.
