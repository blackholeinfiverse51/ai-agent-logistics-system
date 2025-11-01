import React, { useEffect, useState, useMemo, useRef } from 'react';
import { Building2, RefreshCw, Plus, UploadCloud, DownloadCloud, Edit } from 'lucide-react';
import Card, { CardHeader, CardTitle, CardContent, CardFooter } from '../components/common/ui/Card';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../components/common/ui/Table';
import Button from '../components/common/ui/Button';
import Input from '../components/common/forms/Input';
import Badge from '../components/common/ui/Badge';
import Modal, { ModalFooter } from '../components/common/ui/Modal';
import Alert from '../components/common/ui/Alert';
import { LoadingSpinner } from '../components/common/ui/Spinner';

const API_BASE = '';

export const Suppliers = () => {
  const [loading, setLoading] = useState(true);
  const [suppliers, setSuppliers] = useState([]);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null); // { type, message }

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState(null);
  const [form, setForm] = useState({
    supplier_id: '',
    name: '',
    contact_email: '',
    contact_phone: '',
    api_endpoint: '',
    lead_time_days: 7,
    minimum_order: 1,
    is_active: true,
  });

  const fileInputRef = useRef();

  const headers = useMemo(() => {
    const token = localStorage.getItem('token');
    const h = { 'Content-Type': 'application/json' };
    if (token) h['Authorization'] = `Bearer ${token}`;
    return h;
  }, []);

  useEffect(() => {
    fetchSuppliers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchSuppliers = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/procurement/suppliers`, { headers });

      // read raw text first (covering both JSON and HTML error pages)
      const text = await res.text();
      const contentType = (res.headers.get('content-type') || '').toLowerCase();

      if (!res.ok) {
        // If the response is JSON, try to parse the error message
        if (contentType.includes('application/json')) {
          try {
            const parsed = JSON.parse(text);
            throw new Error(parsed.detail || parsed.message || `Failed to load suppliers: ${res.status} ${res.statusText}`);
          } catch (e) {
            throw new Error(`Failed to load suppliers: ${res.status} ${res.statusText}`);
          }
        }

        // Non-OK and not JSON (likely HTML) — include a snippet so user can see what's being returned
        const snippet = text ? text.slice(0, 800) : `${res.status} ${res.statusText}`;
        throw new Error(`Unexpected response from server (status ${res.status}): ${snippet}`);
      }

      // If content-type isn't JSON, show the start of the body to help debugging (common cause: returned HTML index page)
      if (!contentType.includes('application/json')) {
        // Try parsing anyway, but protect against '<!doctype' HTML
        try {
          const parsed = JSON.parse(text);
          setSuppliers(parsed.suppliers || []);
          setNotification({ type: 'success', message: 'Suppliers loaded' });
        } catch (e) {
          const snippet = text ? text.slice(0, 800) : '<empty response>';
          throw new Error(`Expected JSON but received non-JSON response. Response preview: ${snippet}`);
        }
      } else {
        // Normal JSON path
        const data = JSON.parse(text);
        setSuppliers(data.suppliers || []);
        setNotification({ type: 'success', message: 'Suppliers loaded' });
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
      setNotification({ type: 'warning', message: 'Failed to load suppliers — showing cached view' });
    } finally {
      setLoading(false);
    }
  };

  const openAddModal = () => {
    setEditingSupplier(null);
    setForm({ supplier_id: '', name: '', contact_email: '', contact_phone: '', api_endpoint: '', lead_time_days: 7, minimum_order: 1, is_active: true });
    setIsModalOpen(true);
  };

  const openEditModal = (supplier) => {
    setEditingSupplier(supplier.supplier_id || supplier.supplierId || supplier.id);
    setForm({
      supplier_id: supplier.supplier_id || supplier.supplierId || supplier.id,
      name: supplier.name || '',
      contact_email: supplier.contact_email || supplier.contactEmail || '',
      contact_phone: supplier.contact_phone || supplier.contactPhone || '',
      api_endpoint: supplier.api_endpoint || supplier.apiEndpoint || '',
      lead_time_days: supplier.lead_time_days || supplier.leadTimeDays || 7,
      minimum_order: supplier.minimum_order || supplier.minimumOrder || 1,
      is_active: supplier.is_active ?? true,
    });
    setIsModalOpen(true);
  };

  const saveSupplier = async () => {
    try {
      // Basic validation
      if (!form.supplier_id || !form.name) {
        setNotification({ type: 'warning', message: 'Supplier ID and Name are required' });
        return;
      }

      if (editingSupplier) {
        // Update
        const res = await fetch(`${API_BASE}/procurement/suppliers/${editingSupplier}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(form),
        });
        if (!res.ok) throw new Error('Update failed');
        const data = await res.json();
        setSuppliers((s) => s.map((it) => ( (it.supplier_id === editingSupplier || it.supplierId === editingSupplier) ? data.supplier || { ...it, ...form } : it )));
        setNotification({ type: 'success', message: 'Supplier updated' });
      } else {
        // Create
        const res = await fetch(`${API_BASE}/procurement/suppliers`, {
          method: 'POST',
          headers,
          body: JSON.stringify(form),
        });
        if (!res.ok) throw new Error('Create failed');
        const data = await res.json();
        setSuppliers((s) => [ ...(data.supplier ? [data.supplier] : [{ ...form }]), ...s ]);
        setNotification({ type: 'success', message: 'Supplier created' });
      }
      setIsModalOpen(false);
    } catch (err) {
      console.error(err);
      setNotification({ type: 'destructive', message: `Save failed: ${err.message}` });
    }
  };

  const exportJSON = () => {
    const payload = JSON.stringify(suppliers, null, 2);
    const blob = new Blob([payload], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `suppliers_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setNotification({ type: 'success', message: 'Exported suppliers.json' });
  };

  const handleImport = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const parsed = JSON.parse(e.target.result);
        if (!Array.isArray(parsed)) throw new Error('Expected an array of suppliers');
        setSuppliers((s) => [...parsed, ...s]);
        setNotification({ type: 'success', message: 'Imported suppliers (local view only)' });
      } catch (err) {
        setNotification({ type: 'destructive', message: `Import failed: ${err.message}` });
      }
    };
    reader.readAsText(file);
  };

  const metrics = useMemo(() => {
    const total = suppliers.length;
    const active = suppliers.filter((s) => s.is_active || s.isActive || s.active).length;
    const avgLead = suppliers.reduce((acc, s) => acc + (s.lead_time_days || s.leadTimeDays || 0), 0) / (total || 1);
    return { total, active, avgLead: Math.round(avgLead) };
  }, [suppliers]);

  if (loading) return <LoadingSpinner text="Loading suppliers..." />;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Building2 className="h-8 w-8 text-primary" />
          <div>
            <h1 className="text-3xl font-heading font-bold tracking-tight">Supplier Management</h1>
            <p className="text-muted-foreground">Manage supplier records, import/export, and quick actions</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={fetchSuppliers}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="ghost" onClick={() => fileInputRef.current?.click()}>
            <UploadCloud className="h-4 w-4 mr-2" />
            Import
          </Button>
          <input type="file" ref={fileInputRef} className="hidden" accept="application/json" onChange={(e) => e.target.files?.[0] && handleImport(e.target.files[0])} />
          <Button variant="ghost" onClick={exportJSON}>
            <DownloadCloud className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button onClick={openAddModal}>
            <Plus className="h-4 w-4 mr-2" />
            New Supplier
          </Button>
        </div>
      </div>

      {/* Notification */}
      {notification && (
        <Alert
          variant={notification.type === 'destructive' ? 'destructive' : notification.type}
          title={notification.type === 'success' ? 'Success' : notification.type === 'destructive' ? 'Error' : 'Notice'}
          onClose={() => setNotification(null)}
        >
          {notification.message}
        </Alert>
      )}

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Suppliers</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{metrics.total}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Active Suppliers</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{metrics.active}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Avg Lead Time (days)</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{metrics.avgLead}</p>
          </CardContent>
        </Card>
      </div>

      {/* Suppliers Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">Supplier Catalog</CardTitle>
        </CardHeader>
        <CardContent>
          {error && <p className="text-destructive">{error}</p>}
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Contact Email</TableHead>
                <TableHead>Phone</TableHead>
                <TableHead>Lead Time</TableHead>
                <TableHead>Min Order</TableHead>
                <TableHead>Active</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {suppliers.map((s) => (
                <TableRow key={s.supplier_id || s.supplierId || s.id}>
                  <TableCell className="font-medium">{s.supplier_id || s.supplierId || s.id}</TableCell>
                  <TableCell className="font-semibold">{s.name}</TableCell>
                  <TableCell>{s.contact_email || s.contactEmail || '-'}</TableCell>
                  <TableCell>{s.contact_phone || s.contactPhone || '-'}</TableCell>
                  <TableCell>{s.lead_time_days ?? s.leadTimeDays ?? '-'}</TableCell>
                  <TableCell>{s.minimum_order ?? s.minimumOrder ?? '-'}</TableCell>
                  <TableCell>
                    <Badge variant={s.is_active || s.isActive ? 'success' : 'destructive'}>
                      {s.is_active || s.isActive ? 'Active' : 'Inactive'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Button variant="ghost" size="sm" onClick={() => openEditModal(s)}>
                        <Edit className="h-4 w-4 mr-2" />
                        Edit
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
        <CardFooter>
          <p className="text-sm text-muted-foreground">{suppliers.length} suppliers listed</p>
        </CardFooter>
      </Card>

      {/* Modal - Add / Edit Supplier */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingSupplier ? 'Edit Supplier' : 'Add Supplier'}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input label="Supplier ID" value={form.supplier_id} onChange={(e) => setForm({ ...form, supplier_id: e.target.value })} />
          <Input label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <Input label="Contact Email" value={form.contact_email} onChange={(e) => setForm({ ...form, contact_email: e.target.value })} />
          <Input label="Contact Phone" value={form.contact_phone} onChange={(e) => setForm({ ...form, contact_phone: e.target.value })} />
          <Input label="API Endpoint" value={form.api_endpoint} onChange={(e) => setForm({ ...form, api_endpoint: e.target.value })} />
          <Input label="Lead Time (days)" type="number" value={form.lead_time_days} onChange={(e) => setForm({ ...form, lead_time_days: Number(e.target.value) })} />
          <Input label="Minimum Order" type="number" value={form.minimum_order} onChange={(e) => setForm({ ...form, minimum_order: Number(e.target.value) })} />
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={!!form.is_active} onChange={(e) => setForm({ ...form, is_active: e.target.checked })} />
              <span className="text-sm">Active</span>
            </label>
          </div>
        </div>
        <ModalFooter>
          <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
          <Button onClick={saveSupplier}>{editingSupplier ? 'Save Changes' : 'Create Supplier'}</Button>
        </ModalFooter>
      </Modal>
    </div>
  );
};

export default Suppliers;
