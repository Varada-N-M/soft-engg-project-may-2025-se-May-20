<template>
  <div class="app">
    <div class="character">
      <div class="face">
        <div class="eye left"></div>
        <div class="eye right"></div>
        <div class="mouth"></div>
      </div>
    </div>
    <button class="speak-btn" @click="speak">🎨 Say Hello!</button>
  </div>
</template>

<script setup>
const speak = () => {
  const utterance = new SpeechSynthesisUtterance(
    "Helloo friends! Today we will explore colours!"
  );
  utterance.pitch = 1.5;   // high pitch for child voice
  utterance.rate = 0.90;    // slightly fast for energy
  utterance.volume = 1.0;

  const voices = window.speechSynthesis.getVoices();
  utterance.voice =
    voices.find(v => v.name.toLowerCase().includes("child")) ||
    voices.find(v => v.name.toLowerCase().includes("boy")) ||
    voices.find(v => v.name.toLowerCase().includes("girl")) ||
    voices.find(v => v.lang.startsWith("en")) ||
    null;

  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
};
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #fdfd96, #ffb6c1);
  font-family: "Comic Sans MS", cursive;
  text-align: center;
}

.character {
  width: 150px;
  height: 150px;
  background-color: #ffecb3;
  border-radius: 50%;
  border: 4px solid #fbc02d;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  animation: bounce 2s infinite;
}

.face {
  position: relative;
  width: 100px;
  height: 100px;
}

.eye {
  width: 20px;
  height: 20px;
  background: black;
  border-radius: 50%;
  position: absolute;
  top: 30px;
  animation: blink 4s infinite;
}

.eye.left {
  left: 20px;
}

.eye.right {
  right: 20px;
}

.mouth {
  position: absolute;
  bottom: 20px;
  left: 50%;
  width: 40px;
  height: 20px;
  background: #e53935;
  border-radius: 0 0 40px 40px;
  transform: translateX(-50%);
}

.speak-btn {
  background-color: #ff9f1c;
  border: none;
  padding: 12px 24px;
  margin-top: 25px;
  font-size: 18px;
  border-radius: 20px;
  cursor: pointer;
  color: white;
  transition: background 0.3s;
}
.speak-btn:hover {
  background-color: #ffbf69;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

@keyframes blink {
  0%, 90%, 100% {
    height: 20px;
  }
  95% {
    height: 2px;
  }
}
</style>
