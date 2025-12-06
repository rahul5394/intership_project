let isDarkMode = false;

    function getCurrentTime() {
      const now = new Date();
      return now.toLocaleTimeString('hi-IN', { hour: '2-digit', minute: '2-digit' });
    }

    function addMessage(html, isUser = false) {
      const messagesContainer = document.getElementById('chatMessages');
      const quickReplies = messagesContainer.querySelector('.quick-replies');
      if (quickReplies) quickReplies.remove();

      const messageDiv = document.createElement('div');
      messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

      const avatar = document.createElement('div');
      avatar.className = 'message-avatar';
      avatar.textContent = isUser ? '👤' : '🏥';

      const contentDiv = document.createElement('div');
      contentDiv.className = 'message-content';

      const textDiv = document.createElement('div');
      textDiv.innerHTML = html;

      const timeDiv = document.createElement('div');
      timeDiv.className = 'message-time';
      timeDiv.textContent = getCurrentTime();

      contentDiv.appendChild(textDiv);
      contentDiv.appendChild(timeDiv);
      messageDiv.appendChild(avatar);
      messageDiv.appendChild(contentDiv);
      messagesContainer.appendChild(messageDiv);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function showTyping() {
      const messagesContainer = document.getElementById('chatMessages');
      const typingDiv = document.createElement('div');
      typingDiv.className = 'message bot';
      typingDiv.id = 'typing-indicator';

      const avatar = document.createElement('div');
      avatar.className = 'message-avatar';
      avatar.textContent = '🏥';

      const contentDiv = document.createElement('div');
      contentDiv.className = 'message-content';

      const indicator = document.createElement('div');
      indicator.className = 'typing-indicator active';
      indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

      contentDiv.appendChild(indicator);
      typingDiv.appendChild(avatar);
      typingDiv.appendChild(contentDiv);
      messagesContainer.appendChild(typingDiv);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function hideTyping() {
      const typing = document.getElementById('typing-indicator');
      if (typing) typing.remove();
    }

    async function handleSubmit(e) {
      e.preventDefault();
      const input = document.getElementById('messageInput');
      const btn = document.getElementById('sendButton');
      const msg = input.value.trim();

      if (!msg) return;

      addMessage(msg, true);
      input.value = '';
      btn.disabled = true;
      showTyping();

      try {
        const res = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });

        const data = await res.json();
        hideTyping();
        addMessage(data.reply, false);
      } catch (err) {
        hideTyping();
        addMessage('<p><strong>⚠️ Error:</strong> Sorry I Am Not Abel To Give Any Answer For This Question </p><p>Please Try Later .</p>', false);
        console.error(err);
      } finally {
        btn.disabled = false;
        input.focus();
      }
    }

    document.getElementById('chatForm').addEventListener('submit', handleSubmit);

    document.querySelectorAll('.quick-reply-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.getElementById('messageInput').value = btn.dataset.message;
        document.getElementById('chatForm').dispatchEvent(new Event('submit'));
      });
    });

    document.getElementById('themeToggle').addEventListener('click', () => {
      isDarkMode = !isDarkMode;
      document.body.className = isDarkMode ? 'dark-mode' : 'light-mode';
      document.querySelector('.theme-toggle-slider').textContent = isDarkMode ? '🌙' : '☀️';
    });

    document.getElementById('welcome-time').textContent = getCurrentTime();
