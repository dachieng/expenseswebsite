const usernameField = document.querySelector("#id_username");
const userDiv = document.querySelector("#div_id_username")
const emailField = document.querySelector("#id_email");
const emailDiv = document.querySelector("#div_id_email")
const passwordToogle = document.querySelector("#password-toogle");
const password = document.querySelector("#id_password1");
const register = document.querySelector("#register")

let tag = document.createElement("span");
tag.classList.add("text-danger", "font-weight-bold");

let tag2 = document.createElement("p");
tag2.classList.add("text-danger", "font-weight-bold");


emailField.addEventListener("blur", (e) => {
    const emailVal = e.target.value; //equals the value the user types
    emailField.classList.remove("is-invalid");


    if (emailVal.length > 0) {
        tag2.remove();
        fetch("/authentication/validate-email/", {
                body: JSON.stringify({ email: emailVal }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                emailField.classList.remove("is-invalid")
                if (data.email_exists) {
                    emailField.classList.add("is-invalid");
                    tag2.innerHTML = `<p>${data.email_exists}</p>`
                    emailDiv.appendChild(tag2);

                }
                if (data.invalid_email) {
                    emailField.classList.add("is-invalid");
                    tag2.innerHTML = `<p>${data.invalid_email}</p>`;
                    emailDiv.appendChild(tag2);
                    register.setAttribute("disabled", "disabled")
                } else {
                    register.removeAttribute("disabled")
                }
            });
    }
});


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

passwordToogle.addEventListener("click", () => {
    if (passwordToogle.textContent === "SHOW") {
        passwordToogle.textContent = "HIDE";
        password.setAttribute("type", "text");
    } else {
        passwordToogle.textContent = "SHOW";
        password.setAttribute("type", "password")
    }

})