let stockChart;

window.loadDashboardData = async function() {
    if (document.getElementById('daily-gmv')) await loaddailyGMV();
    if (document.getElementById('daily-item-sold')) await loaddailyItemsSold();
    if (document.getElementById('active_staff')) await loadActiveStaff();
    if (document.getElementById('views')) await loadViews();
    if (document.getElementById('total-stock')) await loadstock();
    if (document.getElementById('stockChart')) await loadStockChart();
    if (document.getElementById('top-employee')) await loadTopEmployees();
    if (document.getElementById('recent-payouts')) await loadRecentPayouts();
    if (document.getElementById('recent-activity')) await loadRecentActivity();
};

async function loaddailyGMV() {
    const now = new Date();
    const today = now.toISOString().split('T')[0];
    const cacheKey = `dashboard_gmv_${today}`;

    let data = window.SessionCache ? window.SessionCache.get(cacheKey) : null;
    if (!data) {
        const { data: resData, error } = await supabaseClient
            .from('Live')
            .select('gmv_amount')
            .eq('session_date', today);

        if (error) {
            console.error('Error fetching daily GMV:', error);
            return;
        }
        data = resData;
        if (window.SessionCache) window.SessionCache.set(cacheKey, data);
    }

    const totalGMV = data.reduce((sum, record) => sum + Number(record.gmv_amount||0), 0);
    const el = document.getElementById('daily-gmv');
    if (el) el.textContent = `RM${totalGMV.toFixed(2)}`;
}

async function loaddailyItemsSold() {
    const now = new Date();
    const today = now.toISOString().split('T')[0];
    const cacheKey = `dashboard_items_sold_${today}`;

    let data = window.SessionCache ? window.SessionCache.get(cacheKey) : null;
    if (!data) {
        const { data: resData, error } = await supabaseClient
            .from('Live')
            .select('items_sold')
            .eq('session_date', today);

        if (error) {
            console.error('Error fetching daily items sold:', error);
            return;
        }
        data = resData;
        if (window.SessionCache) window.SessionCache.set(cacheKey, data);
    }

    const totalItemsSold = data.reduce((sum, record) => sum + Number(record.items_sold||0), 0);
    const el = document.getElementById('daily-item-sold');
    if (el) el.textContent = `${totalItemsSold}`;
}

async function loadActiveStaff() {
    const cacheKey = 'dashboard_active_staff';
    let data = window.SessionCache ? window.SessionCache.get(cacheKey) : null;

    if (!data) {
        const { data: resData, error } = await supabaseClient
            .from('profiles')
            .select('role')
            .eq('role', 'employee');

        if (error) {
            console.error('Error fetching active staff:', error);
            return;
        }
        data = resData;
        if (window.SessionCache) window.SessionCache.set(cacheKey, data);
    }

    const activeStaffCount = data ? data.length : 0;
    const el = document.getElementById('active_staff');
    if (el) el.textContent = `${activeStaffCount}`;
}

async function loadViews() {
    const now = new Date();
    const today = now.toISOString().split('T')[0];
    const cacheKey = `dashboard_views_${today}`;

    let data = window.SessionCache ? window.SessionCache.get(cacheKey) : null;
    if (!data) {
        const { data: resData, error } = await supabaseClient
            .from('Live')
            .select('views')
            .eq('session_date', today);

        if (error) {
            console.error('Error fetching views:', error);
            return;
        }
        data = resData;
        if (window.SessionCache) window.SessionCache.set(cacheKey, data);
    }

    const totalViews = data.reduce((sum, record) => sum + Number(record.views||0), 0);
    const el = document.getElementById('views');
    if (el) el.textContent = `${totalViews}`;
}

async function loadstock(){
    const cacheKey = 'dashboard_stock_summary';
    let data = window.SessionCache ? window.SessionCache.get(cacheKey) : null;

    if (!data) {
        const { data: resData, error } = await supabaseClient
            .from('Product')
            .select('Stock');

        if (error) {
            console.error('Error fetching stock:', error);
            return;
        }
        data = resData;
        if (window.SessionCache) window.SessionCache.set(cacheKey, data);
    }

    const totalStock = data.reduce((sum, record) => sum + Number(record.Stock||0), 0);
    const lowStockCount = data.filter(record => Number(record.Stock||0) < 10 && Number(record.Stock||0) > 0).length;
    const outOfStockCount = data.filter(record => Number(record.Stock||0) === 0).length;

    const lowEl = document.getElementById('low-stock');
    const outEl = document.getElementById('out-of-stock');
    const totalEl = document.getElementById('total-stock');

    if (lowEl) lowEl.textContent = `${lowStockCount}`;
    if (outEl) outEl.textContent = `${outOfStockCount}`;
    if (totalEl) totalEl.textContent = `${totalStock}`;
}

async function loadTopEmployees() {
    const date = new Date();
    const startDate = new Date(date.getFullYear(), date.getMonth(), 1);
    const endDate = new Date(date.getFullYear(), date.getMonth() + 1, 1);

    const formatDate = (d) => {
        const y = d.getFullYear();
        const m = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${y}-${m}-${day}`;
    };

    const cacheKey = `dashboard_top_employees_${formatDate(startDate)}`;
    let topEmployeesData = window.SessionCache ? window.SessionCache.get(cacheKey) : null;

    if (!topEmployeesData) {
        const { data, error } = await supabaseClient
            .from('employee_gmv_summary')
            .select('employee_id, total_gmv')
            .gte('session_date', formatDate(startDate))
            .lt('session_date', formatDate(endDate));

        if (error) {
            console.error('Error fetching top employees:', error);
            return;
        }
        const employeeTotals = {};

        data.forEach(record => {
            const employeeId = record.employee_id;
            const gmv = Number(record.total_gmv) || 0;

            if (!employeeTotals[employeeId]) {
                employeeTotals[employeeId] = 0;
            }

            employeeTotals[employeeId] += gmv;
        });

        topEmployeesData = Object.entries(employeeTotals)
        .map(([employee_id, total_gmv]) => ({
            employee_id,
            total_gmv
        }))
        .sort((a, b) => b.total_gmv - a.total_gmv)
        .slice(0, 5);

        if (window.SessionCache) window.SessionCache.set(cacheKey, topEmployeesData);
    }

    const {data:profile, error:profileError} = await supabaseClient
        .from('profiles')
        .select('userid, username')
        .in('userid', topEmployeesData.map(record => record.employee_id));
    
    const profileMap = {};
    if (profileError) {
        console.error('Error fetching employee profiles:', profileError);
        return;
    }
    profile.forEach(record => {
        profileMap[record.userid] = record.username;
    });

    const topEmployees = topEmployeesData.map(record => profileMap[record.employee_id] || 'N/A');
    if (document.getElementById('top-employee')) document.getElementById('top-employee').textContent = topEmployees[0]|| 'N/A';
    if (document.getElementById('second-employee')) document.getElementById('second-employee').textContent = topEmployees[1] || 'N/A';
    if (document.getElementById('third-employee')) document.getElementById('third-employee').textContent = topEmployees[2] || 'N/A';
    if (document.getElementById('fourth-employee')) document.getElementById('fourth-employee').textContent = topEmployees[3] || 'N/A';
    if (document.getElementById('fifth-employee')) document.getElementById('fifth-employee').textContent = topEmployees[4] || 'N/A';
}

async function loadRecentPayouts() {
    const cacheKey = 'dashboard_recent_payouts';
    let data = window.SessionCache ? window.SessionCache.get(cacheKey) : null;

    if (!data) {
        const { data: resData, error } = await supabaseClient
            .from('Payout')
            .select('payout_id, final_payout, payout_date, employee_id')
            .order('payout_date', { ascending: false })
            .limit(5);

        if (error) {
            console.error('Error fetching recent payouts:', error);
            return;
        }
        data = resData;
        if (window.SessionCache) window.SessionCache.set(cacheKey, data);
    }

    const { data: profileData, error: profileError } = await supabaseClient
        .from('profiles')
        .select('userid, username')
        .in('userid', data.map(record => record.employee_id));
    
    if (profileError) {
        console.error('Error fetching employee profiles:', profileError);
        return;
    }

    const profileMap = {};
    profileData.forEach(record => {
        profileMap[record.userid] = record.username;
    });

    const recentPayoutsBody = document.getElementById('recent-payouts');
    if (!recentPayoutsBody) return;
    recentPayoutsBody.innerHTML = '';

    data.forEach(record => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${record.payout_id}</td>
            <td>${profileMap[record.employee_id] || 'N/A'}</td>
            <td>RM${Number(record.final_payout).toFixed(2)}</td>
            <td>${new Date(record.payout_date).toLocaleDateString()}</td>
        `;
        recentPayoutsBody.appendChild(row);
    });
}

const formatActivityDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

async function loadRecentActivity() {
    const container = document.getElementById("recent-activity");
    if (!container) return;

    container.innerHTML = `
        <div class="text-muted text-center">
            Loading...
        </div>
    `;

    const { data: liveData, error: liveError } =
        await supabaseClient
            .from("Live")
            .select("session_date, items_sold, gmv_amount")
            .order("session_date", { ascending: false })
            .limit(5);

    if (liveError) console.error("Error loading Live:", liveError);

    const { data: payoutData, error: payoutError } =
        await supabaseClient
            .from("Payout")
            .select("employee_name, payout_date, final_payout")
            .order("payout_date", { ascending: false })
            .limit(5);

    if (payoutError) console.error("Error loading Payout:", payoutError);

    const activities = [];

    if (liveData) {
        liveData.forEach(record => {
            activities.push({
                type: "live",
                date: new Date(record.session_date),
                title: "Live Session",
                description: `${record.items_sold || 0} items sold • RM${Number(record.gmv_amount || 0).toFixed(2)} GMV`
            });
        });
    }

    if (payoutData) {
        payoutData.forEach(record => {
            activities.push({
                type: "payout",
                date: new Date(record.payout_date),
                title: `Payout for ${record.employee_name}`,
                description: `RM${Number(record.final_payout || 0).toFixed(2)}`
            });
        });
    }

    activities.sort((a, b) => b.date - a.date);
    const recentActivities = activities.slice(0, 5);

    if (recentActivities.length === 0) {
        container.innerHTML = `<div class="text-muted text-center py-3">No recent activity</div>`;
        return;
    }

    container.innerHTML = recentActivities.map(activity => {
        let icon = activity.type === "live" ? "bi-broadcast" : "bi-cash-stack";
        let iconClass = activity.type === "live" ? "text-success" : "text-primary";

        return `
            <div class="d-flex align-items-start mb-3">
                <div class="me-3 d-flex align-items-center justify-content-center" style="width: 38px; height: 38px; border-radius: 50%; background: #f8f9fa;">
                    <i class="bi ${icon} ${iconClass}" style="font-size: 18px;"></i>
                </div>
                <div class="flex-grow-1">
                    <div class="fw-semibold">${activity.title}</div>
                    <div class="text-muted small">${activity.description}</div>
                    <div class="text-muted small mt-1">${formatActivityDate(activity.date)}</div>
                </div>
            </div>
        `;
    }).join("");
}

async function loadStockChart() {
    const canvas = document.getElementById('stockChart');
    if (!canvas) return;

    const cacheKey = 'dashboard_stock_chart';
    let data = window.SessionCache ? window.SessionCache.get(cacheKey) : null;

    if (!data) {
        const { data: resData, error } = await supabaseClient
            .from('Product')
            .select('Product_name, Stock')
            .order('Stock', { ascending: true })
            .limit(10);

        if (error) {
            console.error('Error fetching stock data for chart:', error);
            return;
        }
        data = resData;
        if (window.SessionCache) window.SessionCache.set(cacheKey, data);
    }

    const productNames = data.map(record => record.Product_name);
    const stockValues = data.map(record => Number(record.Stock||0));

    if (stockChart) {
        stockChart.destroy();
    }
    
    stockChart = new Chart(canvas, {
        type: 'bar',
        data:{
            labels: productNames,
            datasets: [{
                label: 'Stock',
                data: stockValues,
                backgroundColor: stockValues.map(stock => {
                    if (stock <= 10) return "#dc3545";
                    if (stock <= 30) return "#fd7e14";
                    if (stock <= 50) return "#ffc107";
                    return "#198754";
                })
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,   
            plugins: { legend: { display: false } },
            scales: {
                x: { beginAtZero: true, title: { display: true, text: 'Stock' } },
                y: { title: { display: true, text: 'Product Name' } }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    window.loadDashboardData();
});
