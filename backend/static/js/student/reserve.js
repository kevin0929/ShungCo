function confirmReservation() {
    const reserveCheckboxA = document.getElementById('reserveCheckboxA');
    const reserveCheckboxB = document.getElementById('reserveCheckboxB');

    const isReservedA = reserveCheckboxA.checked;
    const isReservedB = reserveCheckboxB.checked;

    alert(`影片A預約狀態: ${isReservedA ? '已預約' : '未預約'}\n影片B預約狀態: ${isReservedB ? '已預約' : '未預約'}`);
}