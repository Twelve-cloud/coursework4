const orderBtns = document.querySelectorAll('.btn-accept');

orderBtns.forEach(btn => {
  btn.addEventListener('click', e => {
    const tr = e.target.parentElement.parentElement;

    const username = tr.firstElementChild.textContent;
    const company = tr.firstElementChild.nextElementSibling.textContent;

    tr.remove();
    delete_order({command: "delete", company: company, username: username})
  });
});

async function delete_order(data) {
    const response = await fetch('/orders', {
        method: "PUT",
        header: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}
