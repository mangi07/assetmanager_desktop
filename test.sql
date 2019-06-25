/*
File: test.sql

Create: 4/29/2019

Description: test queries on db created with import.sql
  Not fully test.
*/


-- set up requisition lookup table
insert into requisition (status) values ('awaiting invoice'),('partial payment'),('paid in full'),('donated');

-- more fields can be added later, some default
insert into asset (asset_id, description) values ('test1', 'test1 desc');

select * from asset;

-- need to create a category to be associated with asset
insert into category (name) values ('category1');

-- associate asset with category
update asset set category_1=1 where id=1;

-- select asset and include its category_1 association
select asset.asset_id, asset.description, category.name from asset inner join category on asset.category_1 = category.id;

-- insert 2nd category name to category table so the following asset query will show asset1
insert into category (name) values ('category2');

-- update asset1 to include category2
update asset set category_2=1 where id=1;

-- select asset and associated category names
select asset.asset_id, asset.description, cat1.name as cat1, cat2.name as cat2 from asset
  left join category cat1 on asset.category_1 = cat1.id
  left join category cat2 on asset.category_2 = cat2.id;

-- select location counts for a particular asset
select asset.asset_id, asset.description, location.description, location_count.count from asset
  inner join location_count on asset.id = location_count.asset
  inner join location on location_count.location = location.id
where asset.asset_id = 'folding-chairs-mity-lite-swiftset';

-- select invoice file paths associated with asset ids
select asset.asset_id, invoice.file_path from asset
inner join asset_invoice on asset_invoice.asset = asset.id
inner join invoice on asset_invoice.invoice = invoice.id;

-- select list of asset-far associations
select asset.asset_id, far.description, account.number, far.pdf from asset
inner join asset_far on asset.id = asset_far.asset
inner join far on asset_far.far = far.id
inner join account on far.account = account.id;

-- select list of asset-invoice associations
select asset.asset_id, asset.description, invoice.number, invoice.file_path from asset
inner join asset_invoice on asset_invoice.asset = asset.id
inner join invoice on asset_invoice.invoice = invoice.id;

-- select number of assets that have invoice associations
select count(distinct asset.asset_id) from asset
inner join asset_invoice on asset_invoice.asset = asset.id;

-- update asset notes and location
update asset set notes = "Cost and dates are estimates.  Previous location: ELC-8" where asset.id = 5736 limit 1;
update location_count set location = 249 where location_count.asset=5736;

-- update multiple locations
-- first get asset ids needed to be updated, then...
update location_count set location = 455
where location_count.asset = 5558 or location_count.asset = 5559 or location_count.asset = 5560 
or location_count.asset = 5561 or location_count.asset = 5562;

-- select all one-to-one related fields for an asset:
select asset.id, asset.asset_id, asset.description, asset.is_current, 
            requisition.status as requisition_status, receiving.status as receiving_status,
            cat_1.name as category_1, cat_2.name as category_2, department.name as department_name,
            asset.model_number, asset.serial_number, asset.bulk_count,
            asset.date_placed, asset.date_removed, asset.date_record_created, asset.date_warranty_expires,
            manufacturer.name as manufacturer_name, supplier.name as supplier_name,
            asset.cost, asset.shipping, asset.cost_brand_new, asset.life_expectancy_years,
            purchase_order.number as purchase_order_number,
            asset.notes, asset.maint_dir
            from asset
            left join requisition on asset.requisition = requisition.id
            left join receiving on asset.receiving = receiving.id
            left join category as cat_1 on asset.category_1 = cat_1.id
            left join category as cat_2 on asset.category_2 = cat_2.id
            left join manufacturer on asset.manufacturer = manufacturer.id
            left join supplier on asset.supplier = supplier.id
            left join purchase_order on asset.purchase_order = purchase_order.id
            left join department on asset.department = department.id
            limit {} offset {};

-- select related fields such as from location
select * from asset
left join location_count on location_count.asset = asset.id
left join location on location_count.location = location.id
where location.description like '%Tiyan-105%';

-- or consider combining m2m's with asset listing query and skipping duplicates when forming list data structure in python
-- eg: asset 1 | related m2m 1
--     asset 2 | related m2m 2
--     asset 3 | related m2m 3 ...would result in something like...
--     assets_list = [ [asset 1, [m2m 1, m2m 2]], [asset 2, [m2m 3]] ]
select asset.asset_id, asset.is_current, asset.description, asset.notes, location.id, location.description, picture.file_path from asset
left join location_count on location_count.asset = asset.id
left join location on location.id = location_count.location
left join asset_picture on asset_picture.asset = asset.id
left join picture on picture.id = asset_picture.picture
where location.description = '211';

-- -----------------------
-- reset tables --
-- -----------------------
delete from asset;
delete from account;
delete from asset_far;
delete from asset_invoice;
delete from asset_picture;
delete from checkout;
delete from category;
delete from department;
delete from far;
delete from invoice;
delete from location;
delete from location_count;
delete from manufacturer;
delete from picture;
delete from purchase_order;
delete from receiving;
delete from requisition;
delete from sqlite_sequence;
delete from supplier;
delete from user;

-- set up requisition lookup table
insert into requisition (status) values ('awaiting invoice'),('partial payment'),('paid in full'),('donated');

insert into receiving (status) values ('shipped'), ('received'), ('placed');