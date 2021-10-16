const usernameField = document.querySelector("#id_username");
const userDiv = document.querySelector("#div_id_username")
const emailDiv = document.querySelector("#div_id_email")
const emailField = document.querySelector("#id_email")

let tag = document.createElement("span");
tag.classList.add("text-danger", "font-weight-bold")


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value; //equals the value the user types
    usernameField.classList.remove("is-invalid");


    if (usernameVal.length > 0) {
        tag.remove()
        fetch("/authentication/validate/", {
                body: JSON.stringify({ username: usernameVal }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                userDiv.classList.remove("is-invalid")
                if (data.username_exists) {
                    usernameField.classList.add("is-invalid");
                    tag.innerHTML = `<p>${data.username_exists}</p>`
                    userDiv.appendChild(tag);

                }
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    tag.innerHTML = `<p>${data.username_error}</p>`
                    userDiv.appendChild(tag)
                }

            });
    }
});

emailField.addEventListener("keyup", (e) => {
    console.log(Hello)
})