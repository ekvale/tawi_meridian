"""
Management command to populate contact database from the comprehensive contact list.

Usage: python manage.py populate_contacts
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError
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

        # Helper function to safely create contacts with email handling
        def create_contact(org, first_name, last_name, email='', **defaults):
            """Create contact, handling empty emails gracefully"""
            try:
                if email:
                    contact, created = Contact.objects.get_or_create(
                        organization=org,
                        email=email,
                        defaults={'first_name': first_name, 'last_name': last_name, **defaults}
                    )
                else:
                    # For contacts without email, use first_name + last_name as lookup
                    contact, created = Contact.objects.get_or_create(
                        organization=org,
                        first_name=first_name,
                        last_name=last_name,
                        email='',
                        defaults=defaults
                    )
                if created:
                    self.stdout.write(f'  Created contact: {contact.get_full_name()}')
                return contact
            except IntegrityError:
                # Contact already exists, try to get it
                if email:
                    contact = Contact.objects.filter(organization=org, email=email).first()
                else:
                    contact = Contact.objects.filter(organization=org, first_name=first_name, last_name=last_name, email='').first()
                if contact:
                    # Update existing contact
                    for key, value in defaults.items():
                        setattr(contact, key, value)
                    contact.save()
                    self.stdout.write(f'  Updated contact: {contact.get_full_name()}')
                return contact
        
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
            defaults={'title': 'Chairman', 'role': 'chairman', 'is_primary': True, 'email': ''}
        )
        Contact.objects.get_or_create(
            organization=mwingi,
            first_name='Christine',
            last_name='Musyoka',
            defaults={'title': 'Supervisor', 'role': 'supervisor', 'email': ''}
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
            email='',
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
            email='',
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
            email='',
            defaults={'title': 'County Executive Committee (CEC) Member', 'role': 'officer', 'is_primary': True}
        )
        Contact.objects.get_or_create(
            organization=kitui_trade,
            first_name='Robert',
            last_name='Ngong\'a',
            email='',
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
            email='',
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
            email='',
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
            email='',
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
            email='',
            defaults={'title': 'Prof., Co-investigator on Kitui mango project', 'role': 'researcher', 'is_primary': True}
        )
        Contact.objects.get_or_create(
            organization=umes,
            first_name='Caleb',
            last_name='Nindo',
            email='',
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
            email='',
            defaults={'title': 'Dr., Lead designer - Chimney solar dryer', 'role': 'researcher', 'is_primary': True}
        )
        Contact.objects.get_or_create(
            organization=ucdavis,
            first_name='James',
            last_name='Thompson',
            email='',
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
            email='',
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

        # 4. CGIAR RESEARCH INSTITUTIONS - TOP PRIORITY
        
        # Alliance of Bioversity International and CIAT - Kenya
        cgiar_alliance, _ = Organization.objects.get_or_create(
            name='Alliance of Bioversity International and CIAT - Kenya',
            defaults={
                'type': research_type,
                'category': top_priority,
                'location': 'Africa Hub, Nairobi, Kenya',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'CGIAR research institution. Co-authored comprehensive Makueni mango value chain study. Active in Eastern Kenya (adjacent to Kitui). Agroecological approach aligns with hybrid system.',
                'key_notes': 'Lead contact for entire Makueni study. Gateway to entire CGIAR network. Active in Eastern Kenya.',
                'contact_strategy': 'Email subject: "Solar-Biomass Mango Processing in Kitui County - Research Collaboration". Mention: Read Makueni study, working on adjacent Kitui County. Request: Meeting to discuss collaboration, potential joint research. Offer: Partnership on expanding study to Kitui, data from your pilot.',
            }
        )
        create_contact(cgiar_alliance, 'Christine G. K.', 'Chege', email='c.chege@cgiar.org', title='Researcher, Co-author, listed as contact person', role='researcher', is_primary=True, key_info='Lead contact for entire Makueni study. Expertise: Mango value chain analysis, agroecology, Eastern Kenya. Priority: TIER 1 - Contact this week.')
        create_contact(cgiar_alliance, 'Kevin', 'Onyango', email='k.onyango@cgiar.org', title='Lead Researcher, Principal Investigator', role='researcher', key_info='Lead author, conducted all field work in Makueni. Deep knowledge of mango value chain actors. Established relationships with cooperatives, county government. Priority: TIER 1 - Contact this week.')
        create_contact(cgiar_alliance, 'Peter', 'Bolo', email='p.bolo@cgiar.org', title='Researcher, Co-author', role='researcher', key_info='Expertise: Agroecology, value chains. Priority: TIER 2')
        create_contact(cgiar_alliance, 'Rosina', 'Wanyama', email='r.wanyama@cgiar.org', title='Researcher, Co-author', role='researcher', key_info='Expertise: Value chains, agroecology. Priority: TIER 2')

        # CGIAR Initiative - Transformational Agroecology
        cgiar_agroecology, _ = Organization.objects.get_or_create(
            name='CGIAR Initiative - Transformational Agroecology (Work Package 3 - Kenya Team)',
            defaults={
                'type': research_type,
                'category': top_priority,
                'location': 'Multiple CGIAR centers, Kenya coordination',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Multi-year, multi-million dollar initiative. Focus on scaling agroecological innovations. Your hybrid solar-biomass = agroecological innovation. Already working in Kenya (Makueni ALL).',
                'website': 'https://www.cgiar.org/initiative/agroecology/',
                'contact_strategy': 'Through Christine Chege (she\'s on Kenya team). Position your project as agroecological innovation. Request inclusion in initiative or partnership.',
            }
        )

        # International Institute of Tropical Agriculture (IITA) - Kenya
        iita, _ = Organization.objects.get_or_create(
            name='International Institute of Tropical Agriculture (IITA) - East Africa Hub',
            defaults={
                'type': research_type,
                'location': 'East Africa Hub, Nairobi, Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'IITA has global reach and funding access. Tropical agriculture expertise. East Africa regional focus.',
                'contact_strategy': 'Reach out after connecting with Christine/Kevin. Request technical consultation on mango processing. Explore IITA funding opportunities.',
            }
        )
        create_contact(iita, 'Aurillia', 'Ndiwa', email='a.ndiwa@cgiar.org', title='Researcher', role='researcher', is_primary=True, key_info='Expertise: Tropical agriculture, horticulture, value chains. Priority: TIER 2')

        # 5. MAKUENI COUNTY GOVERNMENT - MODEL & LESSONS
        
        # Makueni County Fruit Development and Marketing Authority (MCFDMA)
        mcfdma, _ = Organization.objects.get_or_create(
            name='Makueni County Fruit Development and Marketing Authority (MCFDMA)',
            defaults={
                'type': govt_type,
                'category': top_priority,
                'location': 'Kalamba processing plant, Makueni County',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Established 2017 (MCFDMA Act, 2017). EXACT MODEL you need to study. County government-owned processing facility. Cooperative supply model. Capacity: 5 tons/hour (40 tons/day, 800 tons/month). Current processing: 1,000-3,000 tons/season (40% utilization).',
                'key_notes': 'Purchase price: KSh 18-21/kg. Products: Mango purée (planning juice, bottled water). Lessons learned (what worked, what didn\'t). Potential customer for dried mango.',
                'contact_strategy': 'Request through Makueni County Agriculture Department or through Kevin Onyango (CGIAR). Schedule facility tour. Interview: Plant Manager, Operations Manager, Procurement Manager, Quality Control Manager. Priority: TIER 1 - Schedule site visit.',
            }
        )

        # Makueni County Department of Agriculture
        makueni_ag, _ = Organization.objects.get_or_create(
            name='Makueni County Government - Department of Agriculture',
            defaults={
                'type': govt_type,
                'location': 'Makueni County',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Understand county support to mango sector. Learn PPP model (MCFDMA). Extension services coordination. Farmer cooperative support.',
                'contact_strategy': 'Schedule meeting during Kalamba visit. Ask Kevin Onyango for introduction. Request briefing on county mango strategy. Priority: TIER 2',
            }
        )

        # Makueni County Investment Authority
        makueni_investment, _ = Organization.objects.get_or_create(
            name='Makueni County Investment Authority (MCIAA)',
            defaults={
                'type': govt_type,
                'location': 'Makueni County',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Established under MCIAA Act. Promote and coordinate investments in county. Learn investment promotion model, PPP structuring, investor facilitation services.',
                'contact_strategy': 'Through county government. Priority: TIER 3',
            }
        )

        # 6. FARMER COOPERATIVES & ASSOCIATIONS
        
        # Makueni Fruit Processing Cooperative Society Ltd.
        makueni_coop, _ = Organization.objects.get_or_create(
            name='Makueni Fruit Processing Cooperative Society Ltd.',
            defaults={
                'type': coop_type,
                'category': top_priority,
                'location': 'Makueni County',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Largest cooperative in Makueni. Members: 3,500 farmers. Successful aggregation model. Supplier to MCFDMA. Volume: 500 tons/season. Prices: KSh 12-15/kg. Formal structure (registered).',
                'key_notes': 'Model for Kitui cooperatives. Training exchange opportunity. Joint marketing for larger volumes.',
                'contact_strategy': 'Request introduction from Kevin Onyango or MCFDMA. Schedule meeting with cooperative leadership. Request: Coop structure, bylaws, farmer contracts, payment systems. Priority: TIER 1',
            }
        )

        # Kwiminia CBO (Women's Aggregation Group)
        kwiminia_cbo, _ = Organization.objects.get_or_create(
            name='Kwiminia CBO (Women\'s Aggregation Group)',
            defaults={
                'type': coop_type,
                'category': top_priority,
                'location': 'Makueni County',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Women-led CBO. Innovation: Cold storage plant built from local materials! Capacity: 40-50 tons storage. Activities: Buying, grading, sorting, bagging, transport.',
                'key_notes': 'Low-cost cold storage design (CRITICAL for your facility!). Women-led (aligns with WOSB certification). Successful aggregation model. Local materials = replicable.',
                'contact_strategy': 'Request introduction from Kevin Onyango or DNRC. Schedule site visit to cold storage facility. Request: Design plans/specs, construction costs, operating costs, materials list, technical drawings. MUST VISIT - Priority: TIER 1',
            }
        )

        # Association of Kenya Mango Traders (AKMT)
        akmt, _ = Organization.objects.get_or_create(
            name='Association of Kenya Mango Traders (AKMT)',
            defaults={
                'type': private_type,
                'category': top_priority,
                'location': 'Nairobi and Mombasa wholesale markets',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Established 2017. Members: 71+ mango traders (growing annually). READY-MADE DISTRIBUTION NETWORK for dried mango. Markets: Wakulima, City Park, Ngara, Kangemi, Kawangware, Githurai, Kongowea (Nairobi + Mombasa).',
                'key_notes': 'National reach (not just Makueni/Kitui). Advocacy power (county government relations). Bulk purchasing power. Activities: Market access, finance facilitation, trade opportunities, lobbying, industry standards.',
                'contact_strategy': 'Identify AKMT members in Wakulima Market (Nairobi). Request meeting with AKMT leadership. Present dried mango opportunity. Offer: Consistent supply of export-grade dried mango. Priority: TIER 1',
            }
        )

        # 7. NGOs & DEVELOPMENT ORGANIZATIONS
        
        # Drylands Natural Resources Center (DNRC)
        dnrc, _ = Organization.objects.get_or_create(
            name='Drylands Natural Resources Center (DNRC) - Makueni Agroecological Living Landscape (ALL)',
            defaults={
                'type': ngo_type,
                'category': top_priority,
                'location': 'Mbooni sub-county, Makueni County',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Host center for CGIAR Agroecology Initiative. Active in both Makueni AND could expand to Kitui. Activities: Mango seedling production (certified nursery), farmer training (IPM, agroecology, value addition), 16 farmer groups (organized), Moringa production/export facilitation.',
                'key_notes': 'Farmer mobilization expertise. Training infrastructure. Agroecological approach (aligned). CGIAR partner.',
                'contact_strategy': 'Introduction through Kevin Onyango (they hosted CGIAR study). Schedule visit to DNRC center. Meet: Director, Extension team, Farmer group coordinators. Explore: Expansion to Kitui County. Priority: TIER 1',
            }
        )

        # TechnoServe - YieldWise Program (update existing)
        if technoserve:
            technoserve.priority = 'critical'
            technoserve.category = top_priority
            technoserve.key_notes = 'Rockefeller Foundation funding precedent. Active next door (Makueni). Exact same mission (post-harvest loss reduction). Could expand to Kitui or co-fund. Market access expertise. Priority: TIER 1 - Contact within 2 weeks'
            technoserve.contact_strategy = 'Email: Reference YieldWise success in Makueni. Propose: Expansion to Kitui with your technology. Offer: Superior hybrid tech vs. existing solar-only. Request: Meeting to discuss partnership. Phone: +254 20 2712020 (Nairobi office)'
            technoserve.save()

        # 8. PRIVATE SECTOR PROCESSORS
        
        # Kevian Kenya Ltd.
        kevian, _ = Organization.objects.get_or_create(
            name='Kevian Kenya Ltd.',
            defaults={
                'type': private_type,
                'location': 'Thika, Central Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Large commercial processor. Products: Mango juice, pulp. Sources From: Muranga, Embu, Machakos, Makueni. National reach.',
                'contact_strategy': 'Request meeting with procurement manager. Present: Dried mango opportunity or fresh supply from Kitui. Ask: Quality specs, volume requirements, pricing. Priority: TIER 2',
                'website': 'www.kevian.co.ke',
            }
        )

        # Sunny Mango
        sunny_mango, _ = Organization.objects.get_or_create(
            name='Sunny Mango',
            defaults={
                'type': private_type,
                'location': 'Thika, Central Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Dried mango producer (direct competitor/potential partner). Products: Dried mango, juice. Model: Nucleus farm + contract farmers. Sources From: Muranga, Embu, Machakos, Makueni. Export market access.',
                'contact_strategy': 'Competitive intelligence (what\'s their pricing, quality, markets?). Potential partnership (you supply, they market). Learn contract farming model. Priority: TIER 2',
            }
        )

        # Milly - Coast Processing
        milly_coast, _ = Organization.objects.get_or_create(
            name='Milly - Coast Processing',
            defaults={
                'type': private_type,
                'location': 'Coast region (Mombasa area)',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Products: Pulp, juice, concentrates (only Kenyan firm doing concentrates). Sources From: Coast production zone (Ngowe variety). Specialty: Concentrates for COMESA regional market.',
                'contact_strategy': 'Explore mango concentrate opportunity. Potential Partnership: Fresh mango supply or concentrate production. Priority: TIER 3',
            }
        )

        # Allfruits
        allfruits, _ = Organization.objects.get_or_create(
            name='Allfruits',
            defaults={
                'type': private_type,
                'location': 'Miritini Export Processing Zone, Mombasa',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Export focus. Requirement: Export most production (EPZ rules). Products: Processed mango for export.',
                'contact_strategy': 'Export market collaboration. Potential Partnership: Export channel for your dried mango. Priority: TIER 3',
            }
        )

        # 9. RESEARCH INSTITUTIONS
        
        # ICRAF/World Agroforestry
        icraf, _ = Organization.objects.get_or_create(
            name='International Centre for Research in Agroforestry (ICRAF/World Agroforestry)',
            defaults={
                'type': research_type,
                'location': 'Nairobi, Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'CIFOR-ICRAF merged. Mentioned in study: Mango diversity research, stakeholder in Makueni. Expertise: Agroforestry, mango varieties, integrated systems.',
                'website': 'www.cifor-icraf.org',
                'contact_strategy': 'Request: Technical consultation on mango agroforestry. Explore: Research collaboration. Priority: TIER 2',
            }
        )

        # ICIPE - Integrated Pest Management
        icipe, _ = Organization.objects.get_or_create(
            name='International Centre of Insect Physiology and Ecology (ICIPE) - IPM Program',
            defaults={
                'type': research_type,
                'category': top_priority,
                'location': 'Nairobi, Kenya (HQ), field sites in Makueni',
                'priority': 'critical',
                'status': 'prospect',
                'description': 'Mentioned in study: Fruit fly IPM research in Makueni. Expertise: Fruit fly control (pheromone traps), biological pest management, farmer training on IPM, Fruit Fly Free Zones (FFFZ) initiative.',
                'key_notes': 'Critical for farmer training (pest management). Active in Makueni, could work in Kitui. Fruit fly = #1 cause of post-harvest losses. FFFZ program = county-level initiative.',
                'website': 'www.icipe.org',
                'contact_strategy': 'Request meeting with IPM program lead. Ask: Expansion of FFFZ to Kitui. Explore: Integrated support (you process, they control pests). Priority: TIER 1',
            }
        )

        # 10. FINANCIAL INSTITUTIONS
        
        # Juhudi Kilimo
        juhudi, _ = Organization.objects.get_or_create(
            name='Juhudi Kilimo',
            defaults={
                'type': financial_type,
                'location': 'Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Microfinance institution. Mentioned in study: Provides credit to Makueni farmers. Specialty: Agricultural loans.',
                'website': 'www.juhudikilimo.com',
                'contact_strategy': 'Explore: Loan products for mango farmers in Kitui. Partnership: Your farmers get preferential loans. Priority: TIER 2',
            }
        )

        # 11. GOVERNMENT AGENCIES
        
        # Ministry of Agriculture, Livestock, Fisheries & Cooperatives - ASCU
        moalfc_ascu, _ = Organization.objects.get_or_create(
            name='Ministry of Agriculture, Livestock, Fisheries & Cooperatives - Agricultural Sector Coordination Unit (ASCU)',
            defaults={
                'type': govt_type,
                'location': 'Nairobi, Kilimo House',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'National level. Role: Inter-ministerial coordination, policy formulation. Mentioned in study: Led development of horticulture policy.',
                'contact_strategy': 'After county-level partnerships established. Information Needed: National mango sector strategy, county support programs. Priority: TIER 3',
            }
        )

        # Horticultural Crops Development Authority (HCDA)
        hcda, _ = Organization.objects.get_or_create(
            name='Horticultural Crops Development Authority (HCDA)',
            defaults={
                'type': govt_type,
                'location': 'Nairobi',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Role: Regulation, development, data collection for horticulture. Data Source: Kenya mango production statistics (cited in study).',
                'website': 'www.hcda.or.ke',
                'contact_strategy': 'Request: Mango sector briefing. Ask: Kitui County production data. Explore: Support programs for processors. Priority: TIER 2',
            }
        )

        # Kenya Plant Health Inspectorate Services (KEPHIS)
        kephis, _ = Organization.objects.get_or_create(
            name='Kenya Plant Health Inspectorate Services (KEPHIS) - FFFZ Program',
            defaults={
                'type': govt_type,
                'location': 'Kenya',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Program: FFFZ (Fruit Fly Free Zones) initiative. Role: Pest control, export certification, quality standards. Mentioned in study: Leading FFFZ campaign in Makueni with county government.',
                'website': 'www.kephis.org',
                'contact_strategy': 'Request: FFFZ program details for Kitui. Ask: Certification requirements for processing facility. Explore: Partnership on farmer training. Priority: TIER 2',
            }
        )

        # 12. EXPORTERS & MARKET ACTORS
        
        # Fresh Produce Exporters Association of Kenya (FPEAK)
        fpeak, _ = Organization.objects.get_or_create(
            name='Fresh Produce Exporters Association of Kenya (FPEAK)',
            defaults={
                'type': private_type,
                'location': 'Nairobi',
                'priority': 'high',
                'status': 'prospect',
                'description': 'Members: Major exporters (Keitt Exporters, Mackay, others). Role: Export facilitation, market intelligence, advocacy.',
                'website': 'www.fpeak.org',
                'contact_strategy': 'Membership inquiry. Export market research. Buyer introductions. Priority: TIER 2',
            }
        )

        # Horticulture Council of Africa (HCA)
        hca, _ = Organization.objects.get_or_create(
            name='Horticulture Council of Africa (HCA)',
            defaults={
                'type': private_type,
                'location': 'Regional (Africa-wide)',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Scope: Regional (Africa-wide). Role: Market development, policy advocacy, capacity building. Mentioned in study: Stakeholder in value chain.',
                'contact_strategy': 'After establishing Kenya operations. Information Needed: COMESA market opportunities for dried mango. Priority: TIER 3',
            }
        )

        # 13. UNIVERSITIES
        
        # University of Machakos
        machakos_univ, _ = Organization.objects.get_or_create(
            name='University of Machakos',
            defaults={
                'type': univ_type,
                'location': 'Machakos County (adjacent to Makueni and Kitui)',
                'priority': 'medium',
                'status': 'prospect',
                'description': 'Local university in mango belt. Mentioned in study: Research stakeholder. Expertise: Agriculture, rural development.',
                'website': 'www.machakosuniversity.ac.ke',
                'contact_strategy': 'Explore research collaboration, student interns. Potential Partnership: Student projects, field trials. Priority: TIER 3',
            }
        )

        self.stdout.write(self.style.SUCCESS(f'\n✅ Total Organizations: {Organization.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Total Contacts: {Contact.objects.count()}'))
