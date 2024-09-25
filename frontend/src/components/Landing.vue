<template>
    <div class="container landing  align-item-center">
        <div class="row py-5 mt-5">
            <div class="col-md-12 col-12 d-flex text-center">
                <h1 class="animate-charcter text-wrap">Welcome To Blog Lite Application</h1>
            </div>
        </div>
        <div class="row butt d-flex justify-content-center p-5">
            <div class="col-md-4 col-lg-4 col-12  text-center align-content-center mb-3 pb-3">
                <router-link class="login p-1 p-lg-2" to="/login">Login</router-link>

            </div>
            <div class="col-md-5 col-lg-4 col-12 text-center mb-3 pb-3">
                <router-link class="register p-1 p-lg-2" to="/register">Register</router-link>
            </div>
        </div>
    </div>
</template>

<script >

</script>

<style scoped>
.login {
    background-color: #11cc97;
    box-shadow: #096645 4px 4px 0px;
    border-radius: 8px;
    transition: transform 200ms, box-shadow 200ms;
    width: 40%;
    height: 15%;
    margin: 10%;
    color: #fff;
    text-decoration: none;
}

.register {
    background-color: #11cc97;
    box-shadow: #096645 4px 4px 0px;
    border-radius: 8px;
    transition: transform 200ms, box-shadow 200ms;
    height: 15%;
    width: 40%;
    margin: 10%;
    color: #fff;
    text-decoration: none;
}

.login:active {
    transform: translateY(4px) translateX(4px);
    box-shadow: #096652 0px 0px 0px;
}

.register:active {
    transform: translateY(4px) translateX(4px);
    box-shadow: #096652 0px 0px 0px;
}

.image {
    height: 150%;
    width: 175%;
}

.butt {
    background: rgba(221, 252, 252, 0.36);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    height: 35%;
    width: 100%;
}

.landing {
    height: 120%;
    width: 70%;
}

.animate-charcter {
    text-transform: uppercase;
    background-image: linear-gradient(-225deg,
            #231557 0%,
            #44107a 29%,
            #ff1361 67%,
            #fff800 100%);
    background-size: auto auto;
    background-clip: border-box;
    background-size: 50% auto;
    color: #fff;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: textclip 2s linear infinite;
    display: inline-block;
    font-size: 5vw;
}

@keyframes textclip {
    to {
        background-position: 200% center;
    }
}
</style>