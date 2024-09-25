<template>
    <div>
        <Nav />
        <div class="container-fluid">
            <div class="row">
                <div class="card_style col-lg-6 col-sm-6 col-12 my-5 d-flex justify-content-evenly" v-for="p in post.Posts"
                    :key="p.id">
                    <!-- post -->

                    <div class="card" style="">
                        <div class="card-header">
                            <div class="d-flex justify-content-between">
                                <div class="d-flex">

                                    <GetPorfilePic width="30" height="30" :user_id="p.user_id"></GetPorfilePic>

                                    <!-- <a href="/login" class="align-middle text-decoration-none" style="color: black">
                                       </a> -->
                                    <router-link :to="/other-profile/ + p.user_id" class="text-decoration-none"
                                        style="color: black">
                                        &nbsp;&nbsp;{{ p.user_name }}
                                    </router-link>
                                    <p class="text-end align-top ms-2 fw-light" style="display: inline; font-size: 12px">
                                        {{ p.created_at }} days ago
                                    </p>
                                </div>

                            </div>
                        </div>


                        <!-- <GetPostImage :post_id="p.id" height="400"></GetPostImage> -->

                        <Suspense>
                            <template #default>
                                <GetPostImage :post_id="p.id" height="400"></GetPostImage>

                            </template>
                            <template #fallback>
                                <div class="spinner-grow text-secondary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </template>
                        </Suspense>

                        <div class="card-body">
                            <h5 class="card-title">{{ p.title }}</h5>
                            <p class="card-text">{{ p.description }}</p>
                        </div>

                        <!-- footer -->

                        <div class="card-footer">
                            <div class="d-flex justify-content-around">
                                <div class="button-group">

                                    <LikeButton :postId="p.id" :userId="user.id"></LikeButton>
                                </div>
                                <div class="d-flex">
                                    <!-- <button class="btn btn-outline-info btn-sm" data-bs-toggle="modal"
                                        data-bs-target="#PostModal">
                                        <i class="bi bi-chat"></i> Comment
                                    </button> -->
                                    <router-link :to="/post-comment/ + p.id" class="btn btn-outline btn-sm">
                                        <i class="bi bi-chat"></i> Comment
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Nav from "./Nav.vue";
import LikeButton from "./LikeButton.vue";
import { ref, onMounted, reactive } from "vue";
import VueJwtDecode from 'vue-jwt-decode'
import GetPostImage from "./GetPostImage.vue";
// import GetPostImageComment from "./GetPostImageComment.vue";
import GetPorfilePic from "./GetPorfilePic.vue";

export default {
    name: "Home",
    components: {
        Nav,
        LikeButton,
        GetPostImage,
        GetPorfilePic
    },
    setup() {
        const comment = ref("");
        const post = reactive({
            Posts: []
        });
        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)
        onMounted(async () => {
            const response = await fetch("http://127.0.0.1:5000/api/posts", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    user_id: user.id
                })
            });
            const data = await response.json()
            post.Posts = data
            console.log(post.Posts)
        });

        return {
            post,
            user
        };
    }
};
</script>

<style>
.card {
    background: rgba(230, 253, 253, 0.226);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    width: 75vh;
}

.card:hover {
    width: 77vh;
}
</style>
