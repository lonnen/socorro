/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

create or replace function backfill_signature_counts (
	begindate date, enddate date )
returns boolean
language plpgsql
as $f$
DECLARE thisdate DATE := begindate;
BEGIN

WHILE thisdate <= enddate LOOP

	RAISE INFO 'backfilling %',thisdate;

	DELETE FROM os_signature_counts WHERE report_date = thisdate;
	DELETE FROM product_signature_counts WHERE report_date = thisdate;
	DELETE FROM uptime_signature_counts WHERE report_date = thisdate;
	PERFORM update_os_signature_counts(thisdate, false);
	PERFORM update_product_signature_counts(thisdate, false);
	PERFORM update_uptime_signature_counts(thisdate, false);
	
	thisdate := thisdate + 1;
	
END LOOP;

RETURN TRUE;
END; $f$;