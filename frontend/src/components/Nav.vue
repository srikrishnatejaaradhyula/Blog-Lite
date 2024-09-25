<template>
    <div>
        <header>
            <nav class="navbar navbar-expand-lg bg-body-tertiary">
                <div class="container-fluid px-4">
                    <a class="navbar-brand animate-charcter" href="#">Blog Lite</a>

                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav ms-auto ps-auto">
                            <li class="nav-item px-3">
                                <router-link to="/home" class="nav-link">
                                    <i class="bi bi-house"></i> Home
                                </router-link>
                            </li>
                            <li class="nav-item px-3">
                                <router-link to="/post" class="nav-link">
                                    <i class="bi bi-plus-square"></i> Post
                                </router-link>
                            </li>
                            <li class="nav-item px-3">
                                <router-link to="/follow" class="nav-link">
                                    <i class="bi bi-person-add"></i> Follow
                                </router-link>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle align-middle" href="#" role="button"
                                    data-bs-toggle="dropdown" aria-expanded="false">
                                    <!-- <GetPorfilePic width="30" height="30" :user_id="user.id"></GetPorfilePic> -->

                                    <Suspense>
                                        <template #default>
                                            <GetPorfilePic width="30" height="30" :user_id="user.id"></GetPorfilePic>

                                        </template>
                                        <template #fallback>
                                            <div class="spinner-grow text-secondary" role="status">
                                                <span class="visually-hidden">Loading...</span>
                                            </div>
                                        </template>
                                    </Suspense>

                                    <p class="text-end align-middle ms-2 fw-bolder" style="display: inline">
                                        {{ username }}
                                    </p>
                                </a>
                                <ul class="dropdown-menu">
                                    <li>
                                        <router-link to="/profile" class="nav-link">
                                            <i class="bi bi-person"></i> Profile
                                        </router-link>
                                    </li>
                                    <li><a class="dropdown-item" href="#">Another action</a></li>
                                    <li>
                                        <hr class="dropdown-divider" />
                                    </li>
                                    <li>
                                        <a class="dropdown-item" href="#">

                                        </a>
                                        <button class="dropdown-item btn btn-outline-light" @click="logout()"
                                            style="color: red ;">
                                            <i class="bi bi-box-arrow-left"></i> Logout
                                        </button>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    </div>
</template>    

<script>
// import Notification from './Notification.vue';
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import VueJwtDecode from 'vue-jwt-decode'

import GetPorfilePic from './GetPorfilePic.vue';

export default {
    name: "Nav",
    components: {
        GetPorfilePic
    },
    setup() {
        const imageUrl = ref('')
        const username = ref('')

        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)
        onMounted(async () => {
            const response = await fetch('http://127.0.0.1:5000/api/get_profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    user_id: user.id
                })
            })
            const data = await response.json()

            username.value = data.username
        })

        const router = useRouter()
        const logout = () => {
            localStorage.removeItem('token');

            router.push('/login')
        }
        return {
            logout,
            imageUrl,
            username,
            user

        }
    }

};

</script>

<style scoped>
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
    font-size: 25px;
    font-weight: 600;
}

@keyframes textclip {
    to {
        background-position: 200% center;
    }
}
</style>
