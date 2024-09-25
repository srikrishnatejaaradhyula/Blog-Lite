<template>
    <div class="container ">
        <div class="row d-flex align-items-center mx-0 my-lg-5 my-md-5 my-0">
            <div class="blank col-md-6 col-12 d-flex justify-content-center">
                <!-- <h3>Don't have an account? </h3> -->
                <div class="col-md-12 text-center  align-middle position-absolute top-50 start-50 translate-middle">
                    <h3>Don't have an account? </h3>
                    <router-link class="btn btn-success" to="/register">Register here!</router-link>
                </div>
            </div>
            <div class="login col-md-6 col-12 ">
                <div class="log">
                    <form>
                        <h4 class="col-md-12 text-center ">Login</h4>
                        <div class="form-floating mb-3 col-md-12 ">
                            <input type="email" v-model="email" class="form-control" id="floatingInput" placeholder=" ">
                            <label for="floatingInput">Email address</label>
                        </div>
                        <div class="form-floating col-md-12 ">
                            <input type="password" v-model="password" class="form-control" id="floatingPassword"
                                placeholder=" ">
                            <label for="floatingPassword">Password</label>
                        </div>
                        <div class="col-md-12 text-center pt-3 ">
                            <button type="submit" @click.prevent="handleLoginSubmit" id="butt" class="btn btn-success">
                                <i class="bi bi-box-arrow-in-right"></i>
                                Login
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import VueJwtDecode from 'vue-jwt-decode'



export default {
    name: "Login",
    setup() {
        const email = ref('')
        const password = ref('')
        const router = useRouter()

        const handleLoginSubmit = async () => {
            try {

                const response = await fetch('http://127.0.0.1:5000/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email.value,
                        password: password.value
                    })
                })
                const data = await response.json()
                console.log(data)

                if (response.status === 400) {
                    console.log(response);
                    throw new Error(`${alert(data.error)}`);
                }

                else {
                    const token = data.token
                    localStorage.setItem('token', token)
                    console.log(token)
                        if (response.status === 200) {
                            alert("Login Successful")
                            router.push('/home')
                        }
                        if (response.status === 201) {
                            alert("Please complete your profile")
                            router.push('/complete-profile')
                        }
                }

            }
            catch (error) {
                console.log("hi it's error in login")
                console.log(error)

            }
        }
        return {
            email,
            password,
            handleLoginSubmit,
        }
    },


}

</script>

<style>
.container {
    width: 75%;
    height: 75%;
}

.blank {
    height: 75vh;
    background: rgba(76, 172, 250, 0.36);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.login {
    height: 75vh;
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);

}

.log {
    padding-top: 20vh;
}

.form-floating input[type="text"],
.form-floating input[type="email"],
.form-floating input[type="password"],
.form-floating textarea {
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #a9b0b7;
    background-color: rgba(255, 255, 255, 0);
}
</style>