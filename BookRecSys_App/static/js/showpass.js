function login() {

    let passwordInput2 = document.getElementById('logPass'),
        toggle2 = document.getElementById('logBtn'),
        icon2 = document.getElementById('logEye');

    function togglePassword() {
        if (passwordInput2.type === 'password') {
            passwordInput2.type = 'text';
            icon2.classList.add("fa-eye-slash");
            //toggle.innerHTML = 'hide';
        } else {
            passwordInput2.type = 'password';
            icon2.classList.remove("fa-eye-slash");
            //toggle.innerHTML = 'show';
        }
    }

    function checkInput() {
        //if (passwordInput.value === '') {
        //toggle.style.display = 'none';
        //toggle.innerHTML = 'show';
        //  passwordInput.type = 'password';
        //} else {
        //  toggle.style.display = 'block';
        //}
    }

    toggle2.addEventListener('click', togglePassword, false);
    passwordInput2.addEventListener('keyup', checkInput, false);

}

function registershow() {
    let passwordInput = document.getElementById('regPass'),
        toggle = document.getElementById('regBtn'),
        icon = document.getElementById('regEye');

    function togglePassword() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.add("fa-eye-slash");
            //toggle.innerHTML = 'hide';
        } else {
            passwordInput.type = 'password';
            icon.classList.remove("fa-eye-slash");
            //toggle.innerHTML = 'show';
        }
    }

    function checkInput() {
        //if (passwordInput.value === '') {
        //toggle.style.display = 'none';
        //toggle.innerHTML = 'show';
        //  passwordInput.type = 'password';
        //} else {
        //  toggle.style.display = 'block';
        //}
    }

    toggle.addEventListener('click', togglePassword, false);
    passwordInput.addEventListener('keyup', checkInput, false);

}








