# حكايات نبتة: إزاي الحلقة بتتعمل

- `ep1.html` : المشهد كله (خلفية، شخصيات، كاميرا، مؤثرات) مرسوم بدالة `setT(ثانية)`. الصور بيقراها من فولدر `a/` جنبه (صور الشخصيات المستخرجة من اللعبة).
- `audio.py` : بيبني `audio.wav` (صوت نبتة من `voice/` + موسيقى ومؤثرات متولّدة بالكود، يعني ملكنا ومفيش عليها حقوق) و`env.json` (قوة الصوت في كل فريم، ودي اللي بتحرّك نبتة وهي بتتكلم).
- `render.js` : بيصوّر ٣٠ فريم في الثانية في فولدر `fr/`، وبعدها ffmpeg بيجمعهم مع الصوت:
  `ffmpeg -framerate 30 -i fr/%04d.jpg -i audio.wav -c:v libx264 -pix_fmt yuv420p -crf 27 -tune animation -c:a aac -shortest ../../videos/nabta-ep1.mp4`

## الحلقات
- الحلقة ١ «نبتة والدودة الجعانة»: `ep1.html` + `audio.py` (المشاركة)
- الحلقة ٢ «نبتة وكتكوت والمطرة»: `ep2.html` + `audio2.py` (المطرة بتسقي الزرع، والنضافة بعد اللعب في الطين)

خطوات أي حلقة:
1. `python3 dev/story/assets.py` مرة واحدة (بيطلّع صور الشخصيات في `a/`)
2. `python3 dev/story/audio2.py` (بيعمل `ep2.wav` و`ep2.env.json`)
3. `NODE_PATH=$(npm root -g) node dev/story/render.js ep2.html 51.5` (ولمعاينة لحظات: `... ep2.html 51.5 prev 10 20 30`)
4. ffmpeg يجمع `fr/` مع الصوت في `videos/nabta-ep2.mp4` و`.webm`
