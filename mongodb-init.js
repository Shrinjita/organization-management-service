// MongoDB initialization script
print('Initializing MongoDB for Organization Management Service...');

// Create admin user for application
db.getSiblingDB('admin').createUser({
  user: 'org_admin',
  pwd: '26813829465d0b7df535b99815a9166ff559952247cd6eccc518a6c4abfcb349',
  roles: [
    { role: 'readWrite', db: 'organization_master' },
    { role: 'readWrite', db: 'organization_master' }
  ]
});

print('MongoDB initialization completed.');