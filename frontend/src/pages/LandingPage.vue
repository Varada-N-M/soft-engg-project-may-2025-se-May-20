<template>
    <div class="landing-page">
        <header class="header">
            <h1>Welcome to Our Application</h1>
            <p>Your one-stop solution for everything</p>
        </header>

        <main class="main-content">
            <section class="features">
                <h2>Key Features</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>Feature 1</h3>
                        <p>Description of feature 1</p>
                    </div>
                    <div class="feature-card">
                        <h3>Feature 2</h3>
                        <p>Description of feature 2</p>
                    </div>
                    <div class="feature-card">
                        <h3>Feature 3</h3>
                        <p>Description of feature 3</p>
                    </div>
                </div>
            </section>
        </main>
    </div>
</template>

<script>
export default {
    name: 'LandingPage',
    data() {
        return {
            // Add reactive data here
        }
    },
    methods: {
        // Add methods here
    }
}
</script>

<style scoped>
.landing-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    padding: 40px 0;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px 0;
}

.feature-card {
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    text-align: center;
}
</style>