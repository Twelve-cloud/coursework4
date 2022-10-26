const orderReportBtn = document.getElementById('order-report-btn');
const dataTable = document.getElementById('dataTable');
const priceElements = document.querySelectorAll('.price');

orderReportBtn.addEventListener('click', (e) => {
    let totalPrice = 0;
    priceElements.forEach(el => {
        totalPrice += +el.textContent;
    });
    downloadPdf(totalPrice);
});

function downloadPdf(totalPrice) {
    const serializer = new XMLSerializer();
    let table = serializer.serializeToString(dataTable);

    table += `<h5>Общая стоимость: ${totalPrice}</h5>`;

    const tableContent = htmlToPdfmake(table);
    pdfMake.createPdf({content: tableContent}).download();
}
