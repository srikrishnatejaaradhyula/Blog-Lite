<template>
    <div>
        <Nav />
        <div class="d-flex justify-content-center my-2" >
            <input type="text" v-model="search" placeholder="Search" class="form-control" style="width: min-content;">
        </div>
        <div class="container follo mb-2" v-for="u in filteredPosts" :key="u.id">
            <!-- <div class="container follo" v-for="u in state.users"> -->

            

            <div class="row py-3 ">

                <div class="col d-flex justify-content-end">

                    <GetPorfilePic width="30" height="30" :user_id="u.id"></GetPorfilePic>
                </div>
                <div class="col ">
                    <router-link :to="/other-profile/ + u.id" class="text-decoration-none" style="color: black">
                        {{ u.name }}
                    </router-link>
                </div>
                <div class="col d-flex justify-content-start">
                    <FollowButton :followerId="user.id" :followedId="u.id"></FollowButton>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Nav from './Nav.vue';
import FollowButton from './FollowButton.vue';
import { ref,onMounted, reactive, computed } from 'vue';
import VueJwtDecode from 'vue-jwt-decode'
import GetPorfilePic from './GetPorfilePic.vue';
import { useRouter } from 'vue-router'

export default {
    name: "Follow",
    components: {
        Nav,
        FollowButton,
        GetPorfilePic
    },
    setup() {
        const search = ref("");
        const state = reactive({
            users: []
        });
        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)
        onMounted(async () => {
            const response = await fetch('http://127.0.0.1:5000/api/all_users', {
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                method: 'GET'
            })
            const data = await response.json()
            state.users = data
            console.log("this is state : ", state.users)
        })
        const  filteredPosts =  computed( () => {
            const filter =  state.users.filter(user =>
                user.name.toLowerCase().includes(search.value.toLowerCase())
            ) ;
            return filter;
        });

        return {
            user,
            state,
            filteredPosts,
            search
            // users: state.users
        }
    },

}

</script>

<style>
.follo {
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    width: 70%;
}
</style>