from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# لتحميل المتغيرات البيئية من ملف .env
load_dotenv() 

app = Flask(__name__)
# لتمكين الطلبات من نطاقات مختلفة (موقعك على GitHub Pages)
CORS(app) 

# تهيئة Gemini API باستخدام المفتاح من المتغيرات البيئية
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# اختيار النموذج (gemini-1.5-flash هو خيار جيد للدردشة والتلخيص)
model = genai.GenerativeModel('gemini-1.5-flash')

# *******************************************************************
# ************* أضف معلومات Technost هنا لتخصيص الشات بوت *************
# ************* تم تحديث معلومات الموقع والتواصل الاجتماعي *************
# *******************************************************************
technost_info = """
نحن Technost، شركة رائدة في تقديم حلول تكنولوجيا المعلومات المتكاملة في العراق.
نقدم مجموعة واسعة من الخدمات والمنتجات لعملائنا، بما في ذلك:

خدماتنا الرئيسية:
- **تطوير البرمجيات المخصصة:** بناء تطبيقات ويب وموبايل مبتكرة تلبي احتياجات عملكم الفريدة.
- **استشارات أمن المعلومات والشبكات:** حماية بياناتكم وبنيتكم التحتية من التهديدات السيبرانية.
- **إدارة قواعد البيانات:** تصميم، تنفيذ، وصيانة قواعد البيانات لضمان كفاءة وسلامة بياناتكم.
- **حلول الحوسبة السحابية (Cloud Solutions):** مساعدتكم على الانتقال إلى السحابة وإدارة مواردكم السحابية بفعالية.
- **دعم فني متخصص:** فريق دعم متاح لمساعدتكم في أي وقت.

منتجاتنا (مثال، يمكنك إضافة منتجاتكم الفعلية هنا):
- نظام إدارة علاقات العملاء (CRM) المخصص.
- حلول تخطيط موارد المؤسسات (ERP) المتكاملة.
- بوابات الدفع الإلكتروني الآمنة.

ساعات العمل:
- من الأحد إلى الخميس، من الساعة 9:00 صباحاً حتى 5:00 مساءً.
- أيام العطل الرسمية: مغلقة.

معلومات التواصل:
- البريد الإلكتروني للدعم الفني: support@technost.com
- البريد الإلكتروني للمبيعات: sales@technost.com
- رقم الهاتف الرئيسي: 07812242772
- رقم هاتف الدعم الفني: 07812242772 (يمكنك استخدام نفس الرقم أو رقم آخر للدعم)
- الموقع الإلكتروني: https://mohamad-aied7.github.io/mohamad/ (تم تحديث هذا الرابط)

حسابات وسائل التواصل الاجتماعي:
  - انستغرام: صفحتنا على انستغرام هي technost.iq ويمكنك زيارتها عبر هذا الرابط المباشر: https://www.instagram.com/technost.iq?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==

موقع الشركة:
- حالياً، ليس لدينا مقر شركة ثابت يمكن زيارته مباشرة. لتقديم أفضل خدمة، يمكنكم التواصل معنا عبر القنوات المذكورة أعلاه (هاتف، بريد إلكتروني، وسائل التواصل الاجتماعي) لحجز موعد مباشر أو استشارة. يسعدنا ترتيب لقاء يناسبكم.

الأسئلة الشائعة (يمكنك إضافة المزيد هنا):
- كيف يمكنني طلب عرض سعر لخدمة معينة؟ يرجى التواصل مع فريق المبيعات عبر البريد الإلكتروني sales@technost.com أو زيارة موقعنا.
- هل تقدمون استشارات مجانية؟ نعم، نقدم استشارة أولية مجانية لتقييم احتياجاتكم.
- ما هي مدة تنفيذ المشاريع؟ تعتمد المدة على حجم وتعقيد المشروع، ولكننا نسعى دائماً للتسليم في أقصر وقت ممكن مع الحفاظ على الجودة.
"""
# *******************************************************************

# المسار الذي ستتلقى عليه رسائل الشات
@app.route('/chat', methods=['POST'])
def chat():
    # استخراج رسالة المستخدم والتاريخ والوقت الحاليين من طلب الـ POST بصيغة JSON
    user_message = request.json.get('message')
    current_datetime = request.json.get('current_datetime') # استلام التاريخ والوقت

    # التحقق إذا كانت الرسالة فارغة
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # بناء المطالبة لتضمين شخصية الشات بوت ومعلومات Technost
        prompt = (
            f"أنت شات بوت ذكي ومختص في خدمة عملاء شركة Technost. مهمتك هي الإجابة على استفسارات العملاء بخصوص خدمات ومنتجات Technost. "
            f"كن ودوداً، مفيداً، ومختصراً قدر الإمكان. "
            f"المعلومات الحالية: {current_datetime}. عند الإجابة على أسئلة حول التاريخ أو الوقت أو اليوم الحالي، استخدم هذه المعلومات. "
            f"معلومات عن Technost: {technost_info}\n\n"
            f"سؤال العميل: {user_message}"
        )
        
        # إرسال المطالبة إلى نموذج Gemini وتلقي الرد
        response = model.generate_content(prompt)
        # استخراج النص الفعلي من رد النموذج
        bot_response = response.text 
        return jsonify({"response": bot_response}) # إرسال الرد إلى الواجهة الأمامية
    except Exception as e:
        # في حالة حدوث أي خطأ، طباعة الخطأ وإرسال رسالة خطأ للواجهة الأمامية
        print(f"Error generating content: {e}")
        return jsonify({"error": "Could not generate response", "details": str(e)}), 500

# مسار جديد لتلخيص المحادثة باستخدام Gemini API
@app.route('/summarize', methods=['POST'])
def summarize():
    chat_history = request.json.get('chat_history')
    if not chat_history:
        return jsonify({"error": "No chat history provided"}), 400

    try:
        # بناء المطالبة لنموذج Gemini لطلب التلخيص
        prompt = f"Please summarize the following conversation:\n\n{chat_history}\n\nSummary:"
        response = model.generate_content(prompt)
        summary_text = response.text
        return jsonify({"summary": summary_text})
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return jsonify({"error": "Could not summarize conversation", "details": str(e)}), 500


# هذا الجزء يضمن تشغيل الخادم عند تنفيذ الملف مباشرة
if __name__ == '__main__':
    # تشغيل الخادم على المنفذ 5000 (يمكنك تغييره إذا كان مستخدماً)
    app.run(debug=True, port=5000)
