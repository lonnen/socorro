/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

\set ON_ERROR_STOP 1

alter default privileges for role breakpad_rw grant select on sequences to breakpad;

alter default privileges for role breakpad_rw grant select on tables to breakpad;

grant select on all tables in schema public to breakpad;

grant select on all sequences in schema public to breakpad;

