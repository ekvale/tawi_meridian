"""
Management command to populate contact database from the comprehensive contact list.

Usage: python manage.py populate_contacts
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from project_management.models import (
    Organization, Contact, OrganizationType, ContactCategory
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate organizations and contacts from the comprehensive contact list'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing organizations and contacts before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Contact.objects.all().delete()
            Organization.objects.all().delete()
            ContactCategory.objects.all().delete()
            OrganizationType.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating organization types...'))
        self.create_organization_types()

        self.stdout.write(self.style.SUCCESS('Creating contact categories...'))
        self.create_contact_categories()

        self.stdout.write(self.style.SUCCESS('Creating organizations and contacts...'))
        self.create_organizations_and_contacts()

        self.stdout.write(self.style.SUCCESS('\n✅ Successfully populated contact database!'))
        self.stdout.write(f'Total Organizations: {Organization.objects.count()}')
        self.stdout.write(f'Total Contacts: {Contact.objects.count()}')

    def create_organization_types(self):
        """Create organization types"""
        types_data = [
            {'name': 'Farmer Cooperative', 'description': 'Farmer cooperatives and farmer organizations', 'order': 1},
            {'name': 'Government Agency', 'description': 'Government agencies at county, national, or international level', 'order': 2},
            {'name': 'University', 'description': 'Universities and academic institutions', 'order': 3},
            {'name': 'Research Institution', 'description': 'Research organizations and institutes', 'order': 4},
            {'name': 'Non-profit Organization', 'description': 'Non-profit and NGO organizations', 'order': 5},
            {'name': 'Private Company', 'description': 'Private sector companies and businesses', 'order': 6},
            {'name': 'Foundation', 'description': 'Foundations and funding organizations', 'order': 7},
            {'name': 'Development Agency', 'description': 'International development agencies', 'order': 8},
            {'name': 'Financial Institution', 'description': 'Banks and financial institutions', 'order': 9},
            {'name': 'Media', 'description': 'Media and communications organizations', 'order': 10},
            {'name': 'Export Market', 'description': 'Export buyers and market partners', 'order': 11},
            {'name': 'Equipment Supplier', 'description': 'Equipment manufacturers and suppliers', 'order': 12},
        ]

        for type_data in types_data:
            OrganizationType.objects.get_or_create(
                name=type_data['name'],
                defaults={
                    'description': type_data['description'],
                    'display_order': type_data['order']
                }
            )

    def create_contact_categories(self):
        """Create contact categories"""
        categories_data = [
            {'name': 'TOP PRIORITY', 'color': 'red', 'description': 'Must contact immediately', 'order': 1},
            {'name': 'CRITICAL PARTNER', 'color': 'orange', 'description': 'Critical for project success', 'order': 2},
            {'name': 'STRATEGIC PARTNER', 'color': 'blue', 'description': 'Strategic long-term partners', 'order': 3},
            {'name': 'KEY ACADEMIC PARTNER', 'color': 'purple', 'description': 'Important academic collaborators', 'order': 4},
            {'name': 'PRIMARY FUNDER', 'color': 'green', 'description': 'Primary funding sources', 'order': 5},
            {'name': 'PROVEN FUNDER', 'color': 'teal', 'description': 'Funders with track record in sector', 'order': 6},
        ]

        for cat_data in categories_data:
            ContactCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'color': cat_data['color'],
                    'description': cat_data['description'],
                    'display_order': cat_data['order']
                }
            )

    def create_organizations_and_contacts(self):
        """Create organizations and their contacts"""
        
        # Get or create types
        coop_type, _ = OrganizationType.objects.get_or_create(name='Farmer Cooperative')
        govt_type, _ = OrganizationType.objects.get_or_create(name='Government Agency')
        univ_type, _ = OrganizationType.objects.get_or_create(name='University')
        research_type, _ = OrganizationType.objects.get_or_create(name='Research Institution')
        ngo_type, _ = OrganizationType.objects.get_or_create(name='Non-profit Organization')
        private_type, _ = OrganizationType.objects.get_or_create(name='Private Company')
        foundation_type, _ = OrganizationType.objects.get_or_create(name='Foundation')
        dev_agency_type, _ = OrganizationType.objects.get_or_create(name='Development Agency')
        financial_type, _ = OrganizationType.objects.get_or_create(name='Financial Institution')
        media_type, _ = OrganizationType.objects.get_or_create(name='Media')
        export_type, _ = OrganizationType.objects.get_or_create(name='Export Market')
        supplier_type, _ = OrganizationType.objects.get_or_create(name='Equipment Supplier')

        # Get or create categories
        top_priority, _ = ContactCategory.objects.get_or_create(name='TOP PRIORITY')
        critical_partner, _ = ContactCategory.objects.get_or_create(name='CRITICAL PARTNER')
        strategic_partner, _ = ContactCategory.objects.get_or_create(name='STRATEGIC PARTNER')
        key_academic, _ = ContactCategory.objects.get_or_create(name='KEY ACADEMIC PARTNER')
        primary_funder, _ = ContactCategory.objects.get_or_create(name='PRIMARY FUNDER')
        proven_funder, _ = ContactCategory.objects.get_or_create(name='PROVEN FUNDER')

        # 1. KITUI COUNTY - LOCAL PARTNERS & COOPERATIVES
        
        # Mwingi Horticulture Farmers' Cooperative Society
        mwingi, _ = Organization.objects.get_or_create(
            name="Mwingi Horticulture Farmers' Cooperative Society",
            defaults={
                'type': coop_type,
                'category': top_priority,
                'location': 'Mwingi sub-county, Kitui County',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Farmer cooperative with 70+ members, serves 1,000+ farmers. Existing solar processing plant (KSh 8M, installed 2017).',
                'key_notes': 'Low processing capacity - explicitly requesting more dryers. Products: Mango flakes, juice, jam, dried fruits. Perfect pilot partner.',
                'contact_strategy': 'Reach out through Kitui County Government. Visit facility during next mango season. Proposal: Upgrade/expand their system with hybrid technology.',
            }
        )
        Contact.objects.get_or_create(
            organization=mwingi,
            first_name='Sammy',
            last_name='Mwanthi Kibwana',
            defaults={'title': 'Chairman', 'role': 'chairman', 'is_primary': True}
        )
        Contact.objects.get_or_create(
            organization=mwingi,
            first_name='Christine',
            last_name='Musyoka',
            defaults={'title': 'Supervisor', 'role': 'supervisor'}
        )

        # Mbitini Ward Farmers Sacco
        mbitini, _ = Organization.objects.get_or_create(
            name='Mbitini Ward Farmers Sacco',
            defaults={
                'type': coop_type,
                'category': top_priority,
                'location': 'Mbitini Ward, Kitui County',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Received 2 solar dryers in February 2022. Collected 110 tonnes mangoes in 2021-2022 season.',
                'key_notes': 'Poor quality dryers, couldn\'t access markets. They have demand but poor technology - need upgrade.',
                'contact_strategy': 'Offer technology assessment and upgrade proposal.',
            }
        )
        Contact.objects.get_or_create(
            organization=mbitini,
            first_name='Kwithya',
            last_name='',
            defaults={'title': 'Chairperson (also Secretary of Mbitini Horticulture Cooperative Society Limited)', 'role': 'chairman', 'is_primary': True}
        )

        # Mosa Mango Growers
        mosa, _ = Organization.objects.get_or_create(
            name='Mosa Mango Growers',
            defaults={
                'type': coop_type,
                'location': 'Kitui County',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Active group focused on sustainability. Partners: Etimos Foundation, Switch Africa Green.',
                'key_notes': 'Participated in sustainable mango training (2019). Focused on sustainability - aligned values.',
                'contact_strategy': 'Contact through Etimos Foundation or UNEP Switch Africa Green.',
            }
        )
        Contact.objects.get_or_create(
            organization=mosa,
            first_name='Christine',
            last_name='Makomba',
            defaults={'title': 'Key Member', 'is_primary': True}
        )

        # Kitui Enterprise Promotion Company Limited (KEPC)
        kepc, _ = Organization.objects.get_or_create(
            name='Kitui Enterprise Promotion Company Limited (KEPC)',
            defaults={
                'type': private_type,
                'category': strategic_partner,
                'location': 'Kitui County',
                'priority': 'critical',
                'status': 'partner',
                'description': 'Social enterprise founded 2012. Serves 800+ farmers. Products: Mango juice, powder, flakes, fortified flour.',
                'key_notes': 'Supported by USAID Farmer-to-Farmer program, National Environment Trust Fund. Impact: Farmers earning $500-800/season. Challenge: Marketing capacity, needs to scale.',
                'contact_strategy': 'Explore partnership - you provide processing tech, they provide market channels. Based in Kitui, works through cooperative model.',
            }
        )
        Contact.objects.get_or_create(
            organization=kepc,
            first_name='Crack',
            last_name='Munyao',
            defaults={'title': 'Managing Director', 'role': 'director', 'is_primary': True}
        )

        # Kitui County Government - Office of the Governor
        kitui_govt, _ = Organization.objects.get_or_create(
            name='Kitui County Government - Office of the Governor',
            defaults={
                'type': govt_type,
                'category': critical_partner,
                'location': 'Kitui County',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'County actively investing in agricultural value addition. Invested KSh 20M in fruit processing machine (2020).',
                'key_notes': 'Built juice processing factory for Mwingi Horticulture Cooperative. Constructed 16 honey processing factories for beekeepers. Supported 32 Saccos.',
                'contact_strategy': 'Submit proposal for county co-funding. Position as aligned with county development goals. Emphasize job creation and farmer income.',
            }
        )

        # Department of Trade, Industry, ICT and Cooperatives Development
        kitui_trade, _ = Organization.objects.get_or_create(
            name='Kitui County Government - Department of Trade, Industry, ICT and Cooperatives Development',
            defaults={
                'type': govt_type,
                'category': critical_partner,
                'location': 'Kitui County',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Directly responsible for cooperative development and value addition. Recent activity: Ushirika Day celebrations.',
                'contact_strategy': 'Request meeting to present proposal. Ask about county cooperative support programs. Explore PPP opportunities.',
            }
        )
        Contact.objects.get_or_create(
            organization=kitui_trade,
            first_name='Jonah',
            last_name='Mwinzi',
            defaults={'title': 'County Executive Committee (CEC) Member', 'role': 'officer', 'is_primary': True}
        )
        Contact.objects.get_or_create(
            organization=kitui_trade,
            first_name='Robert',
            last_name='Ngong\'a',
            defaults={'title': 'Director', 'role': 'director'}
        )

        # Department of Agriculture, Livestock and Fisheries
        kitui_ag, _ = Organization.objects.get_or_create(
            name='Kitui County Government - Department of Agriculture, Livestock and Fisheries',
            defaults={
                'type': govt_type,
                'category': critical_partner,
                'location': 'Kitui County',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Technical support, extension services, farmer mobilization.',
                'contact_strategy': 'Partnership for farmer training and extension services.',
            }
        )
        Contact.objects.get_or_create(
            organization=kitui_ag,
            first_name='Redemptory',
            last_name='Mary',
            defaults={'title': 'Director of Special Programs (supported Mwingi facility)', 'role': 'director', 'is_primary': True}
        )

        # Sun Sweet Fruit Farm Products Limited
        sunsweet, _ = Organization.objects.get_or_create(
            name='Sun Sweet Fruit Farm Products Limited',
            defaults={
                'type': private_type,
                'location': 'Ithiani village, Changwithya West, Kitui County',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Works with 80+ farmers. Products: Mango flakes (exported to France), jam, soap, lip balms. Technology: Solar drying.',
                'key_notes': 'Capital investment: KSh 5.2 million (2019). Challenges: Insufficient financial resources, slow market penetration, requisite equipment, lack of optimum infrastructure. Export market connections (2 French companies).',
                'contact_strategy': 'Offer technology assessment. Potential partnership: You provide tech, they provide market access. Learn about export compliance requirements.',
            }
        )
        Contact.objects.get_or_create(
            organization=sunsweet,
            first_name='Simon',
            last_name='Musyoka',
            defaults={'title': 'Owner/Founder', 'role': 'director', 'is_primary': True}
        )

        # 2. NATIONAL RESEARCH INSTITUTIONS & UNIVERSITIES
        
        # Jomo Kenyatta University of Agriculture and Technology (JKUAT)
        jkuat, _ = Organization.objects.get_or_create(
            name='Jomo Kenyatta University of Agriculture and Technology (JKUAT)',
            defaults={
                'type': univ_type,
                'category': key_academic,
                'location': 'Kenya',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Already working in Kitui on mango project. Has USAID connection. Currently focusing on production, needs processing solution.',
                'key_notes': '2024 project in Kitui County. Expertise: Mango value chain, farmer training, extension services.',
                'contact_strategy': 'Propose collaboration: IPM (their expertise) + Processing (your solution). Joint research/demonstration project. Potential for joint publications.',
            }
        )
        Contact.objects.get_or_create(
            organization=jkuat,
            first_name='Evelyn',
            last_name='Okoth',
            defaults={'title': 'Dr., Lead researcher, Kitui mango IPM project', 'role': 'researcher', 'is_primary': True}
        )

        # University of Maryland Eastern Shore (UMES)
        umes, _ = Organization.objects.get_or_create(
            name='University of Maryland Eastern Shore (UMES)',
            defaults={
                'type': univ_type,
                'category': key_academic,
                'location': 'United States',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Co-investigators on Kitui mango project. US university connection valuable for USAID DIV application.',
                'contact_strategy': 'Research collaboration. Potential letter of support for DIV application. Technical advisory.',
            }
        )
        Contact.objects.get_or_create(
            organization=umes,
            first_name='Stephen',
            last_name='Tubene',
            defaults={'title': 'Prof., Co-investigator on Kitui mango project', 'role': 'researcher', 'is_primary': True}
        )
        Contact.objects.get_or_create(
            organization=umes,
            first_name='Caleb',
            last_name='Nindo',
            defaults={'title': 'Prof., Co-investigator on Kitui mango project, Food processing expertise', 'role': 'researcher'}
        )

        # UC Davis Horticulture Innovation Lab
        ucdavis, _ = Organization.objects.get_or_create(
            name='University of California, Davis - Horticulture Innovation Lab',
            defaults={
                'type': univ_type,
                'category': key_academic,
                'location': 'United States',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Chimney solar dryer design (used in Kenya, Tanzania, Ghana). Free manual and design specifications available. Open source design.',
                'contact_strategy': 'Download their manual (baseline design). Reach out for technical consultation. Explain your hybrid biomass innovation. Potential collaboration: Next-generation hybrid version of their design.',
            }
        )
        Contact.objects.get_or_create(
            organization=ucdavis,
            first_name='Michael',
            last_name='Reid',
            defaults={'title': 'Dr., Lead designer - Chimney solar dryer', 'role': 'researcher', 'is_primary': True}
        )
        Contact.objects.get_or_create(
            organization=ucdavis,
            first_name='James',
            last_name='Thompson',
            defaults={'title': 'Dr., Lead designer - Chimney solar dryer', 'role': 'researcher'}
        )

        # University of Minnesota
        umn, _ = Organization.objects.get_or_create(
            name='University of Minnesota',
            defaults={
                'type': univ_type,
                'category': key_academic,
                'location': 'United States',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'CEO\'s home institution. Department of Mechanical Engineering. Focus: Renewable energy, sustainable technology, international development.',
                'contact_strategy': 'CEO to reach out to former advisors/faculty. Explore research collaboration or student projects.',
            }
        )

        # Makerere University (Uganda)
        makerere, _ = Organization.objects.get_or_create(
            name='Makerere University (Uganda)',
            defaults={
                'type': univ_type,
                'category': key_academic,
                'location': 'Uganda',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Designed hybrid solar dryer (8m×4m×2m). Capacity: 300 kg fresh fruit/batch, 20 kg dried/batch. Innovation: Sensor-controlled dual heat source (solar + biomass).',
                'key_notes': 'Location: Kangulumira, Kayunga district, Uganda. Partner: Kisega Horticulture Association.',
                'contact_strategy': 'Academic exchange. Compare designs. Potential regional partnership.',
            }
        )
        Contact.objects.get_or_create(
            organization=makerere,
            first_name='Simon Savio',
            last_name='Kizito',
            defaults={'title': 'Dr., Designer of hybrid solar dryer', 'role': 'researcher', 'is_primary': True}
        )

        # KALRO - Kenya Agricultural and Livestock Research Organization
        kalro, _ = Organization.objects.get_or_create(
            name='Kenya Agricultural and Livestock Research Organization (KALRO)',
            defaults={
                'type': research_type,
                'location': 'Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'National research authority. Key finding: 40-45% post-harvest losses for mangoes. Recommendation: Establishment of certified propagation centers in Kitui.',
                'contact_strategy': 'Request technical collaboration and technology validation.',
            }
        )

        # KEFRI - Kenya Forestry Research Institute
        kefri, _ = Organization.objects.get_or_create(
            name='Kenya Forestry Research Institute (KEFRI)',
            defaults={
                'type': research_type,
                'location': 'Kitui County, Kenya',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Conducted farmers\' technology preference survey in Kitui (1999). Identified mango as priority, introduced improved varieties (2000). Varieties: Apple, Ngowe, Haden, Kent, Sabine, Tommy Atkins, Van Dyke.',
                'contact_strategy': 'Learn from their farmer engagement model.',
            }
        )

        # 3. USAID & DEVELOPMENT PARTNERS
        
        # USAID Kenya Mission - Agriculture Office
        usaid_kenya, _ = Organization.objects.get_or_create(
            name='USAID Kenya Mission - Agriculture Office',
            defaults={
                'type': dev_agency_type,
                'category': primary_funder,
                'location': 'Nairobi, Kenya',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Established presence in Kitui mango sector. Multiple successful projects. Programs: Feed the Future, agricultural development, value chains.',
                'key_notes': 'Track record in Kitui: Funded Mwingi facility (2017). Supporting JKUAT mango IPM project. Farmer-to-Farmer program (KEPC support).',
                'contact_strategy': 'Attend USAID partner meetings. Connect with agriculture program officers. Reference existing Kitui mango investments.',
            }
        )

        # USAID Development Innovation Ventures (DIV)
        usaid_div, _ = Organization.objects.get_or_create(
            name='USAID Development Innovation Ventures (DIV)',
            defaults={
                'type': dev_agency_type,
                'category': primary_funder,
                'location': 'Washington DC, United States',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Rolling submissions year-round. Funding: Stage 1 ($150-200K), Stage 2 ($1.5M), Stage 3 ($15M). Perfect fit for your project.',
                'contact_strategy': 'Submit online application. Emphasize post-harvest loss reduction. Highlight scalability and cost-effectiveness. Use Kitui data: 40-50% losses, 100,000+ tonnes wasted.',
            }
        )

        # Rockefeller Foundation
        rockefeller, _ = Organization.objects.get_or_create(
            name='Rockefeller Foundation',
            defaults={
                'type': foundation_type,
                'category': proven_funder,
                'location': 'United States',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'YieldWise Initiative. Funded mango post-harvest loss reduction in Kenya (TechnoServe partnership). Multi-year, multi-million program.',
                'key_notes': 'Counties: Embu, Machakos, Meru, Tharaka Nithi, Makueni, Tana River, Kwale, Elgeyo Marakwet. Note: Kitui NOT in original YieldWise counties - opportunity for expansion!',
                'contact_strategy': 'Position as YieldWise expansion into Kitui (leading mango county). Emphasize innovation (hybrid technology). Connect through TechnoServe (their implementing partner).',
            }
        )

        # TechnoServe Kenya
        technoserve, _ = Organization.objects.get_or_create(
            name='TechnoServe Kenya',
            defaults={
                'type': ngo_type,
                'location': 'Nairobi, Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Rockefeller YieldWise implementing partner. Expertise: Value chain development, farmer aggregation, market linkages.',
                'key_notes': 'Cited for Kenya mango production estimates (400-500K tonnes).',
                'contact_strategy': 'Explore partnership as technical assistance provider.',
            }
        )

        # Catholic Relief Services (CRS)
        crs, _ = Organization.objects.get_or_create(
            name='Catholic Relief Services (CRS) - East Africa Farmer-to-Farmer Program',
            defaults={
                'type': ngo_type,
                'location': 'Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Supported KEPC since 2014. Services: Business development, marketing, technical volunteers. Funding: USAID.',
                'contact_strategy': 'Apply for technical volunteer support.',
            }
        )

        # UN Women Kenya
        un_women, _ = Organization.objects.get_or_create(
            name='UN Women Kenya',
            defaults={
                'type': ngo_type,
                'location': 'Nairobi, Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Supported mango farmer training in Kenya (2018). Funded multi-food processing machine (7.8 tonnes/6 hours). Focus: Women\'s economic empowerment.',
                'key_notes': 'Beneficiary example: Teresa Kawira (45, mother of 7) - mango farmer. Many mango farmers are women.',
                'contact_strategy': 'Emphasize women beneficiaries, gender lens.',
            }
        )

        # FAO Kenya
        fao, _ = Organization.objects.get_or_create(
            name='FAO (Food and Agriculture Organization) Kenya',
            defaults={
                'type': ngo_type,
                'location': 'Nairobi, Kenya',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Post-harvest loss statistics (30-40%). Programs: Food security, value chains, sustainable agriculture.',
                'contact_strategy': 'Explore technical cooperation.',
            }
        )

        # UNEP
        unep, _ = Organization.objects.get_or_create(
            name='UNEP (UN Environment Programme)',
            defaults={
                'type': ngo_type,
                'location': 'Nairobi, Kenya',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Switch Africa Green program (supported Mosa Mango Growers). Partner: Etimos Foundation. Focus: Green economy, sustainable consumption/production.',
                'contact_strategy': 'Position as green economy innovation.',
            }
        )

        # Additional foundations and organizations
        gates_foundation, _ = Organization.objects.get_or_create(
            name='Bill & Melinda Gates Foundation',
            defaults={
                'type': foundation_type,
                'location': 'United States',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Large-scale funder for agricultural innovation. Focus: Agricultural development, smallholder farmers, food security.',
                'contact_strategy': 'Monitor grant opportunities, potential for scaling phase.',
            }
        )

        mastercard_foundation, _ = Organization.objects.get_or_create(
            name='Mastercard Foundation',
            defaults={
                'type': foundation_type,
                'location': 'Canada',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Focus: Youth employment, agriculture, financial inclusion. Program: Young Africa Works. Major presence in Kenya.',
                'contact_strategy': 'Position as youth employment + financial inclusion project.',
            }
        )

        # Export Markets
        east_african_growers, _ = Organization.objects.get_or_create(
            name='East African Growers',
            defaults={
                'type': export_type,
                'location': 'Kenya',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Export focus. Products: Dried mango, fresh mango.',
                'contact_strategy': 'Introduce yourself as future supplier of export-grade dried mango.',
            }
        )

        # Equipment Suppliers
        grainpro, _ = Organization.objects.get_or_create(
            name='GrainPro (Philippines/Global)',
            defaults={
                'type': supplier_type,
                'location': 'Philippines',
                'priority': 'low',
                'status': 'prospect',
                'description': 'Solar tunnel dryers. Used in Ethiopia cooperatives project. Capacity: 200-1,000 kg/day models.',
                'contact_strategy': 'Request specifications and pricing for equipment comparison.',
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Created {Organization.objects.count()} organizations'))
        self.stdout.write(self.style.SUCCESS(f'Created {Contact.objects.count()} contacts'))
