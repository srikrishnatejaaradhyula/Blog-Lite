<template>
    <div class="container profile">
        <div class="row  align-items-center">
            <div class="col-md-6 col-lg-6 col-12">
                <div class="upload-img">
                    <label class="custom-file-upload">

                        <input type="file" @input="onFileSelected">
                        <img :src="imageUrl" v-if="imageUrl" height="150" width="150" style="clip-path: circle();">
                        <!-- <div v-else>
                            <GetPorfilePic width="150" height="150" :user_id="ids"></GetPorfilePic>
                        </div> -->
                        <i class="bi bi-camera" v-else style="font-size: 6rem; color: #ced4da;"></i>
                    </label>
                </div>
                <h6 class="">Upload Profile Pic</h6>
            </div>
            <div class="col-md-6 col-lg-6 col-12 ">
                <div class="form-floating col-md-12 mb-4">
                    <input type="text" class="form-control" v-model="username" id="floatingInput" placeholder=" "
                        required />
                    <label for="floatingInput">Username</label>
                </div>
                <div class="form-floating col-12 mb-4">
                    <textarea class="form-control" v-model="description" placeholder="Leave a comment here"
                        id="floatingTextarea"></textarea>
                    <label for="floatingTextarea"> Description </label>
                </div>
            </div>
        </div>
        <div class="row mt-1">
            <div class="col align-content-end">
            </div>
            <button class="btn btn-success" style="width: min-content;" @click.prevent="UpdateProfile">
                Save
            </button>
        </div>
        <div class="row mt-1">
            <div class="col align-content-start  mt-5">
                <router-link to="/profile" class="btn btn-success" style="width: max-content;">
                    Go Back
                </router-link>
            </div>
            <!-- <button class="btn btn-success" style="width: min-content;" @click="SaveProfile()">
                Save
            </button> -->

        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import VueJwtDecode from 'vue-jwt-decode'
import GetPorfilePic from './GetPorfilePic.vue'

export default {
    name: "CompleteProfile",
    components: {
        GetPorfilePic
    },

    setup() {
        const imageUrl = ref(null);
        const file = ref(null);
        const username = ref(null);
        const description = ref(null);
        const isImage = ref(null);
        const router = useRouter()

        const route = useRoute()
        const ids = computed(() => route.params.id);

        console.log("this is id", ids.value)

        const onFileSelected = (e) => {

            file.value = e.target.files[0];
            const reader = new FileReader();
            // reader.readAsDataURL(file.value)
            reader.onload = e => {
                imageUrl.value = e.target.result;
            };
            reader.readAsDataURL(file.value);
        }

        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)


        const UpdateProfile = async () => {
             
            const reader = new FileReader()
            reader.readAsDataURL(file.value)
            reader.onload = async () => {
                const base64 = reader.result.split(',')[1]

                console.log("this is base64", base64)

                try {

                    const response = await fetch('http://127.0.0.1:5000/api/update_profile', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'x-access-tokens': localStorage.getItem('token')
                        },
                        // body: formData
                        body: JSON.stringify({
                            // isImage: isImage.value,
                            image: base64,
                            username: username.value,
                            description: description.value,
                            user_id: user.id
                        })
                    })
                    console.log(response)
                    const data = await response.json()
                    console.log(data.id)
                    if (response.status === 201) {
                        alert("Profile Updated Successfully!")
                    }

                    if (response.status === 401) {
                        throw new Error(`${alert(data.id)}`);
                    }
                    if (response.status === 400) {
                        throw new Error(`${alert(data.error)}`);
                    }
                }
                catch (error) {
                    console.log(error)
                }
            }

        }

        onMounted(async () => {
            const response1 = await fetch('http://127.0.0.1:5000/api/get_profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    user_id: user.id
                })
            })
            const data1 = await response1.json()
            console.log("onMount data", data1)
            username.value = data1.username
            description.value = data1.description


            const response2 = await fetch('http://127.0.0.1:5000/api/get_profile_img', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    id: user.id
                })
            })
            const blob = await response2.blob()
            const objectUrl = URL.createObjectURL(blob)
            imageUrl.value = objectUrl

           file.value = new File([blob], 'profile.jpg', { type: blob.type });
        })
        return {
            imageUrl,
            file,
            username,
            description,
            onFileSelected,
            UpdateProfile,
            ids,
            isImage
        }
    }
}
</script>

<style>
/* .upload-img {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 28vh;
    border-radius: 50%;
    -moz-border-radius: 50%;
    -webkit-border-radius: 50%;
    width: 14vw;
    border: 2px dashed #74777b
} */

.profile {
    margin-top: 10vh;
    width: 70%;
}
</style>