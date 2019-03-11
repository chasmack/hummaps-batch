
ALTER TABLE hummaps.map
ADD CONSTRAINT maptype_book_page_unique UNIQUE (maptype_id, book, page);