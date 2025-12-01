const defaultConfig = {
      background_color: "#e8f5e3",
      card_color: "#ffffff",
      text_color: "#1a1a1a",
      primary_button_color: "#4CAF50",
      accent_color: "#2196F3",
      app_title: "HealthAI",
      tagline: "Your AI-Powered Health Companion",
      login_button_text: "Log In",
      signup_button_text: "Create Account",
      feature_1: "AI-powered health insights and personalized recommendations",
      feature_2: "Track your vitals and health metrics in real-time",
      feature_3: "Secure and private - your data is encrypted end-to-end"
    };

    let isLoginForm = true;
    let isPasswordVisible = false;

    async function onConfigChange(config) {
      const backgroundColor = config.background_color || defaultConfig.background_color;
      const cardColor = config.card_color || defaultConfig.card_color;
      const textColor = config.text_color || defaultConfig.text_color;
      const primaryButtonColor = config.primary_button_color || defaultConfig.primary_button_color;
      const accentColor = config.accent_color || defaultConfig.accent_color;
      const fontFamily = config.font_family || defaultConfig.font_family;
      const fontSize = config.font_size || defaultConfig.font_size || 16;

      // Apply colors
      document.querySelector('.main-container').style.background = backgroundColor;
      document.querySelector('.left-panel').style.color = textColor;
      document.querySelector('.form-container').style.background = cardColor;
      document.querySelector('.form-container').style.color = textColor;

      /* background ke shaps ko move kara ne ke liae*/
      document.querySelectorAll('.floating-shape').forEach(shape => {
        shape.style.background = accentColor;
      });

      document.querySelectorAll('.feature-item').forEach(item => {
        item.style.background = `${cardColor}99`;
      });

      document.querySelectorAll('.feature-icon').forEach(icon => {
        icon.style.background = `${accentColor}20`;
      });

      document.querySelector('.tab-switcher').style.background = `${textColor}05`;
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.style.color = textColor;
      });

      const activeTab = document.querySelector('.tab-btn.active');
      if (activeTab) {
        activeTab.style.background = primaryButtonColor;
        activeTab.style.color = '#ffffff';
      }

      document.querySelectorAll('.submit-btn').forEach(btn => {
        btn.style.background = primaryButtonColor;
        btn.style.color = '#ffffff';
      });

      document.querySelector('.forgot-link').style.color = accentColor;
      document.querySelector('.success-toast').style.background = primaryButtonColor;
      document.querySelector('.success-toast').style.color = '#ffffff';

      // Apply text content

      // Apply font
      if (fontFamily) {
        document.querySelector('.main-container').style.fontFamily = `${fontFamily}, 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`;
      }

      // Apply font sizes
      document.querySelector('.app-title').style.fontSize = `${fontSize * 2.625}px`;
      document.querySelector('.tagline').style.fontSize = `${fontSize}px`;
      document.querySelector('.form-title').style.fontSize = `${fontSize * 1.75}px`;
      document.querySelector('.form-subtitle').style.fontSize = `${fontSize * 0.8125}px`;
      document.querySelectorAll('.feature-text').forEach(el => el.style.fontSize = `${fontSize * 0.875}px`);
      document.querySelectorAll('.input-label').forEach(el => el.style.fontSize = `${fontSize * 0.75}px`);
      document.querySelectorAll('.form-input').forEach(el => el.style.fontSize = `${fontSize * 0.875}px`);
      document.querySelectorAll('.submit-btn').forEach(el => el.style.fontSize = `${fontSize * 0.9375}px`);
      document.querySelectorAll('.tab-btn').forEach(el => el.style.fontSize = `${fontSize * 0.875}px`);
    }

    function showToast(message) {
      const toast = document.getElementById('successToast');
      const toastMessage = document.getElementById('toastMessage');
      toastMessage.textContent = message;
      toast.classList.add('show');

      setTimeout(() => {
        toast.classList.remove('show');
      }, 3000);
    }

    // Tab switching
    document.getElementById('loginTab').addEventListener('click', () => {
      isLoginForm = true;
      document.getElementById('loginForm').style.display = 'block';
      document.getElementById('signupForm').style.display = 'none';
      document.getElementById('loginTab').classList.add('active');
      document.getElementById('signupTab').classList.remove('active');

      const config = window.elementSdk?.config || defaultConfig;
      const primaryColor = config.primary_button_color || defaultConfig.primary_button_color;
      const textColor = config.text_color || defaultConfig.text_color;

      document.getElementById('loginTab').style.background = primaryColor;
      document.getElementById('loginTab').style.color = '#ffffff';
      document.getElementById('signupTab').style.background = 'transparent';
      document.getElementById('signupTab').style.color = textColor;

      document.querySelector('.form-title').textContent = 'Welcome Back';
      document.querySelector('.form-subtitle').textContent = 'Access your health dashboard';
    });

    document.getElementById('signupTab').addEventListener('click', () => {
      isLoginForm = false;
      document.getElementById('loginForm').style.display = 'none';
      document.getElementById('signupForm').style.display = 'block';
      document.getElementById('signupTab').classList.add('active');
      document.getElementById('loginTab').classList.remove('active');

            //login se sign up par jo green color jata

      const config = window.elementSdk?.config || defaultConfig;
      const primaryColor = config.primary_button_color || defaultConfig.primary_button_color;
      const textColor = config.text_color || defaultConfig.text_color;
      document.getElementById('signupTab').style.background = primaryColor;
      document.getElementById('signupTab').style.color = '#ffffff';
      document.getElementById('loginTab').style.background = 'transparent';
      document.getElementById('loginTab').style.color = textColor;

       });

    // Password toggle for login card
    document.getElementById('loginToggle').addEventListener('click', function() {
      const input = document.getElementById('loginPassword');
      if (input.type === 'password') {
        input.type = 'text';
        this.textContent = '🙈';
      } else {
        input.type = 'password';
        this.textContent = '👁️';
      }
    });

    // Password toggle for sign-up card
    document.getElementById('signupToggle').addEventListener('click', function() {
      const input = document.getElementById('signupPassword');
      if (input.type === 'password') {
        input.type = 'text';
        this.textContent = '🙈';
      } else {
        input.type = 'password';
        this.textContent = '👁️';
      }
    });

    onConfigChange(defaultConfig);
