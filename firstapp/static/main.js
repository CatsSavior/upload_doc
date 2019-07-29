function copyHtml() {
    const html_for_copy = document.getElementById("html_for_copy");
    /* Select the text field */
    html_for_copy.select();

    /* Copy the text inside the text field */
    document.execCommand("copy");
}

setTimeout(copyHtml, 3);