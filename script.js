document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const messagesContainer = document.getElementById('messages');
    const newChatButton = document.getElementById('new-chat-button');
    const summarizeButton = document.getElementById('summarize-button');

    let chatHistory = []; // مصفوفة لتخزين سجل المحادثة

    // دالة لإضافة رسالة لواجهة الشات
    function appendMessage(sender, text) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = text;
        messagesContainer.appendChild(messageElement);
        // ننزل ليجوه حتى نشوف آخر رسالة
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // إضافة الرسالة إلى سجل المحادثة
        chatHistory.push({ sender: sender, text: text });
    }

    // دالة لإزالة رسالة "جاري الكتابة..."
    function removeLoadingMessage() {
        const lastMessage = messagesContainer.lastElementChild;
        if (lastMessage && lastMessage.textContent === 'جاري الكتابة...') {
            messagesContainer.removeChild(lastMessage);
        }
    }

    // دالة إرسال الرسالة إلى الـ Backend
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '') return; // لا ترسل رسالة فارغة

        appendMessage('user', message); // نعرض رسالة المستخدم
        messageInput.value = ''; // نمسح حقل الإدخال

        const backendUrl = 'http://127.0.0.1:5000/chat'; 

        appendMessage('bot', 'جاري الكتابة...'); // عرض رسالة "جاري الكتابة..."
        
        try {
            // الحصول على التاريخ والوقت الحاليين
            const now = new Date();
            const currentDateTime = now.toLocaleString('ar-EG', {
                weekday: 'long', // اليوم من الأسبوع
                year: 'numeric', // السنة
                month: 'long', // الشهر
                day: 'numeric', // اليوم من الشهر
                hour: 'numeric', // الساعة
                minute: 'numeric', // الدقائق
                second: 'numeric', // الثواني
                hour12: true // لتنسيق AM/PM
            });

            const response = await fetch(backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // إرسال رسالة المستخدم والتاريخ والوقت الحاليين
                body: JSON.stringify({ message: message, current_datetime: currentDateTime }) 
            });

            removeLoadingMessage(); // نوخر رسالة التحميل

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, details: ${errorData.error || 'Unknown error'}`);
            }

            const data = await response.json();
            appendMessage('bot', data.response); // نعرض رد البوت
        } catch (error) {
            console.error('Error sending message to backend:', error);
            removeLoadingMessage(); 
            appendMessage('bot', 'عذراً، حدث خطأ أثناء الاتصال بالخادم. الرجاء المحاولة لاحقاً.');
        }
    }

    // دالة لتلخيص المحادثة
    async function summarizeChat() {
        if (chatHistory.length === 0) {
            appendMessage('bot', 'لا توجد محادثة لتلخيصها.');
            return;
        }

        // تحضير سجل المحادثة لإرساله إلى الـ Backend
        const conversationText = chatHistory.map(msg => `${msg.sender}: ${msg.text}`).join('\n');
        
        const summarizeUrl = 'http://127.0.0.1:5000/summarize';

        appendMessage('bot', '✨ جاري تلخيص المحادثة...');

        try {
            const response = await fetch(summarizeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ chat_history: conversationText })
            });

            removeLoadingMessage(); // إزالة رسالة التحميل

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, details: ${errorData.error || 'Unknown error'}`);
            }

            const data = await response.json();
            appendMessage('bot', 'ملخص المحادثة: ' + data.summary); // عرض الملخص
        } catch (error) {
            console.error('Error summarizing chat:', error);
            removeLoadingMessage();
            appendMessage('bot', 'عذراً، حدث خطأ أثناء تلخيص المحادثة. الرجاء المحاولة لاحقاً.');
        }
    }

    // دالة لمسح جميع الرسائل من الشات وبدء محادثة جديدة
    function clearChat() {
        messagesContainer.innerHTML = ''; // مسح كل المحتوى داخل div الرسائل
        chatHistory = []; // مسح سجل المحادثة
        appendMessage('bot', 'مرحباً! كيف يمكنني مساعدتك اليوم؟'); // رسالة ترحيبية لبداية محادثة جديدة
    }

    // إضافة مستمعي الأحداث لزر الإرسال وضغط Enter
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // إضافة مستمع الحدث لزر "محادثة جديدة"
    newChatButton.addEventListener('click', clearChat);

    // إضافة مستمع الحدث لزر "تلخيص المحادثة"
    summarizeButton.addEventListener('click', summarizeChat);

    // رسالة ترحيبية عند تحميل الصفحة لأول مرة
    appendMessage('bot', 'مرحباً! كيف يمكنني مساعدتك اليوم؟');
});
